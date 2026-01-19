# src/orchestration/ops/scrape.py
from dagster import op
from src.scraping.scrapper import main as run_scraper  # replace `main` with the actual function name

@op
def scrape_telegram_data():
    """Scrape Telegram messages"""
    run_scraper()
