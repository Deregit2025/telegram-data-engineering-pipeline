
import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

def get_telegram_client():
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    session_name = os.getenv("SESSION_NAME", "telegram_scraper_session")
    
    return TelegramClient(session_name, api_id, api_hash)
