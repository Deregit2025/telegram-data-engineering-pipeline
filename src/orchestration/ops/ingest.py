# src/orchestration/ops/ingest.py
from dagster import op
from src.ingestion.load_telegram_messages import load_json_files

@op
def load_raw_to_postgres():
    """Load all raw Telegram messages into PostgreSQL"""
    load_json_files()
