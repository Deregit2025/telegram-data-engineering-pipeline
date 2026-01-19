# src/ingestion/load_telegram_messages.py

import json
from pathlib import Path
import logging
from src.ingestion.db import get_connection, create_raw_schema, db_conf

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Path to JSON files (search recursively in case of date folders)
MESSAGES_FOLDER = Path(__file__).parent.parent.parent / "data" / "raw" / "messages"

def create_raw_table():
    """
    Create the raw.telegram_messages table if it doesn't exist
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_conf['raw_schema']}.telegram_messages (
                message_id TEXT PRIMARY KEY,
                channel_name TEXT,
                post_date TIMESTAMP,
                message_text TEXT,
                view_count INTEGER,
                forward_count INTEGER,
                has_image BOOLEAN,
                raw_json JSONB
            );
        """)
        conn.commit()
        logger.info("Table 'raw.telegram_messages' ensured in database.")
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        raise

def load_json_files():
    """
    Read all JSON files in data/raw/messages/ (including subfolders)
    and insert into PostgreSQL
    """
    create_raw_schema()
    create_raw_table()

    json_files = list(MESSAGES_FOLDER.rglob("*.json"))
    if not json_files:
        logger.warning(f"No JSON files found in {MESSAGES_FOLDER}")
        return

    for json_file in json_files:
        logger.info(f"Loading file: {json_file.name}")
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error reading {json_file.name}: {e}")
                continue

        conn = get_connection()
        cursor = conn.cursor()

        inserted_count = 0
        for msg in messages:
            try:
                cursor.execute(f"""
                    INSERT INTO {db_conf['raw_schema']}.telegram_messages
                    (message_id, channel_name, post_date, message_text, view_count, forward_count, has_image, raw_json)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (message_id) DO NOTHING;
                """, (
                    str(msg.get("message_id")),           # Correct key
                    msg.get("channel_name"),
                    msg.get("message_date"),              # Correct key
                    msg.get("message_text"),
                    msg.get("views", 0),                  # Correct key
                    msg.get("forwards", 0),               # Correct key
                    bool(msg.get("has_media")),           # Correct key
                    json.dumps(msg)
                ))
                inserted_count += 1
            except Exception as e:
                logger.error(f"Error inserting message {msg.get('message_id')}: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Loaded {inserted_count} messages from {json_file.name}")

if __name__ == "__main__":
    load_json_files()
    logger.info("All JSON files loaded successfully!")
