# src/orchestration/ops/yolo_ops.py
from dagster import op
from src.yolo_detect import main as run_yolo  # import the main() function

@op
def run_yolo_enrichment():
    """Run YOLOv8 object detection on images"""
    run_yolo()
