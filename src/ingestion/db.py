# src/ingestion/db.py

import psycopg2
import yaml
import logging
from pathlib import Path

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load database configuration
CONFIG_FILE = Path(__file__).parent.parent.parent / "config" / "database_config.yaml"

with open(CONFIG_FILE) as f:
    config = yaml.safe_load(f)

db_conf = config["postgres"]

def get_connection():
    """
    Returns a psycopg2 connection to PostgreSQL
    """
    try:
        conn = psycopg2.connect(
            host=db_conf["host"],
            port=db_conf["port"],
            user=db_conf["user"],
            password=db_conf["password"],
            dbname=db_conf["database"]
        )
        return conn
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
        raise

def create_raw_schema():
    """
    Create raw schema if it doesn't exist
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {db_conf['raw_schema']};")
        conn.commit()
        logger.info(f"Schema '{db_conf['raw_schema']}' ensured in database.")
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        raise
