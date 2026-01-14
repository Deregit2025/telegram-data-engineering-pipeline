import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()


def get_telegram_client():
    """
    Creates and returns an authenticated Telegram client.
    """
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    session_name = os.getenv("TELEGRAM_SESSION_NAME", "telegram_scraper_session")

    return TelegramClient(session_name, api_id, api_hash)
