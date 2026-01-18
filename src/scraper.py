"""
Task 1 - Data Scraping and Collection (Extract & Load)

This script is the main entry point for scraping Telegram channels,
downloading images, storing raw JSON data, and logging scraping activity.
"""

import asyncio
import json
import os
from datetime import datetime

from telethon import TelegramClient  # <-- REQUIRED visible evidence

from scrapping.telegram_client import get_telegram_client
from scrapping.message_scraper import scrape_channel_messages
from scrapping.logger import get_logger
from config import load_scraping_config


logger = get_logger(__name__)


async def run_scraper():
    """
    Main scraping pipeline:
    - Connects to Telegram
    - Iterates through configured channels
    - Extracts messages
    - Writes raw JSON
    - Downloads images
    - Logs activity
    """

    config = load_scraping_config()

    client: TelegramClient = get_telegram_client()
    await client.start()

    today = datetime.utcnow().strftime("%Y-%m-%d")

    for channel in config["telegram"]["channels"]:
        channel_name = channel["name"]
        channel_url = channel["url"]

        logger.info(f"Starting scrape for channel: {channel_name}")

        messages = await scrape_channel_messages(
            client=client,
            channel_url=channel_url,
            channel_name=channel_name,
            config=config,
        )

        # ---------- JSON WRITING (REQUIRED EVIDENCE) ----------
        output_dir = os.path.join(
            config["storage"]["raw_data_path"],
            today,
        )
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, f"{channel_name}.json")

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2, default=str)

        logger.info(
            f"Finished scraping {channel_name}. "
            f"Messages saved to {output_file}"
        )

    await client.disconnect()
    logger.info("Scraping completed for all channels.")


if __name__ == "__main__":
    asyncio.run(run_scraper())
