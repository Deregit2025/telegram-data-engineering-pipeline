import time
import logging
from telethon.errors import FloodWaitError


def handle_rate_limit(error: FloodWaitError):
    """
    Handles Telegram FloodWait errors by sleeping.
    """
    wait_seconds = error.seconds
    logging.warning(f"Rate limit hit. Sleeping for {wait_seconds} seconds.")
    time.sleep(wait_seconds)
