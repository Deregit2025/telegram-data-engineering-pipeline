"""
Task 1 - Data Scraping and Collection (Extract & Load)

This script is the main entry point for scraping Telegram channels,
downloading images, storing raw JSON data, and logging scraping activity.
"""

import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List

from telethon import TelegramClient, errors  # type: ignore

from scrapping.telegram_client import get_telegram_client
from scrapping.message_scraper import scrape_channel_messages
from scrapping.logger import get_logger
from config import load_scraping_config

logger = get_logger(__name__)


async def run_scraper() -> None:
    """
    Main scraping pipeline:
    - Connects to Telegram
    - Iterates through configured channels
    - Extracts messages
    - Writes raw JSON to disk
    - Logs scraping activity

    Raises:
        RuntimeError: If Telegram connection fails or messages cannot be fetched.
    """

    config: Dict[str, Any] = load_scraping_config()

    try:
        client: TelegramClient = get_telegram_client()
        await client.start()
    except errors.TelegramError as e:
        logger.exception("Failed to start Telegram client.")
        raise RuntimeError("Telegram client initialization failed") from e

    today: str = datetime.utcnow().strftime("%Y-%m-%d")
    raw_data_path: str = config["storage"].get("raw_data_path", "data/raw")

    for channel in config.get("telegram", {}).get("channels", []):
        channel_name: str = channel.get("name")
        channel_url: str = channel.get("url")

        if not channel_name or not channel_url:
            logger.warning(f"Skipping channel with incomplete configuration: {channel}")
            continue

        logger.info(f"Starting scrape for channel: {channel_name}")

        try:
            messages: List[Dict[str, Any]] = await scrape_channel_messages(
                client=client,
                channel_url=channel_url,
                channel_name=channel_name,
                config=config,
            )
        except Exception as e:
            logger.exception(f"Failed to scrape messages for channel {channel_name}")
            continue

        # ---------- JSON WRITING ----------
        output_dir: str = os.path.join(raw_data_path, today)
        os.makedirs(output_dir, exist_ok=True)

        output_file: str = os.path.join(output_dir, f"{channel_name}.json")
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2, default=str)
        except OSError as e:
            logger.exception(f"Failed to write messages to {output_file}")
            continue

        logger.info(
            f"Finished scraping {channel_name}. Messages saved to {output_file}"
        )

    try:
        await client.disconnect()
    except errors.TelegramError:
        logger.warning("Error disconnecting Telegram client, ignoring.")

    logger.info("Scraping completed for all channels.")


if __name__ == "__main__":
    asyncio.run(run_scraper())
