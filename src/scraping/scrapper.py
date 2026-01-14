import asyncio
import json
import yaml
import logging
from pathlib import Path
from datetime import datetime

from telethon.errors import FloodWaitError

from src.scraping.telegram_client import get_telegram_client
from src.scraping.message_scraper import extract_message_data
from src.scraping.rate_limiter import handle_rate_limit
from src.scraping.logger import setup_logger


def load_config():
    with open("config/scraping_config.yaml", "r") as f:
        return yaml.safe_load(f)


def save_raw_messages(messages, base_path, channel_name):
    """
    Saves raw messages as JSON in a date-partitioned folder.
    """
    date_partition = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(base_path) / date_partition
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"{channel_name}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


async def scrape_channel(client, channel, config):
    channel_name = channel["name"]
    channel_url = channel["url"]

    logging.info(f"Starting scrape for channel: {channel_name}")
    messages_data = []

    try:
        async for message in client.iter_messages(
            channel_url,
            limit=config["scraping"]["fetch_limit"]
        ):
            image_path = None

            if message.photo and config["scraping"]["download_images"]:
                image_dir = Path(config["storage"]["image_path"]) / channel_name
                image_dir.mkdir(parents=True, exist_ok=True)

                image_path = image_dir / f"{message.id}.jpg"
                await message.download_media(file=image_path)

            messages_data.append(
                extract_message_data(
                    message=message,
                    channel_name=channel_name,
                    image_path=str(image_path) if image_path else None,
                )
            )

    except FloodWaitError as e:
        handle_rate_limit(e)

    save_raw_messages(
        messages_data,
        config["storage"]["raw_data_path"],
        channel_name,
    )

    logging.info(f"Finished scrape for channel: {channel_name}")


async def main():
    config = load_config()
    setup_logger(config["logging"]["log_path"])

    client = get_telegram_client()

    async with client:
        for channel in config["telegram"]["channels"]:
            await scrape_channel(client, channel, config)


if __name__ == "__main__":
    asyncio.run(main())
