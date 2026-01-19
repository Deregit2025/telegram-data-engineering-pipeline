from dagster import schedule
from .pipeline import telegram_pipeline

@schedule(cron_schedule="0 6 * * *", job=telegram_pipeline, execution_timezone="UTC")
def daily_telegram_pipeline():
    return {}
