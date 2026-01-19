# src/orchestration/pipeline.py
from dagster import job
from src.orchestration.ops.scrape import scrape_telegram_data
from src.orchestration.ops.ingest import load_raw_to_postgres
from src.orchestration.ops.dbt_ops import run_dbt_transformations
from src.orchestration.ops.yolo_ops import run_yolo_enrichment

@job
def telegram_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
