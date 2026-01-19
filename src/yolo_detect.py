"""
YOLO Image Detection Module

Processes raw images from Telegram channels using YOLOv8, classifies images
into categories, and saves detection results to a CSV file.

Outputs:
- CSV file with per-image and per-object detection results
"""

import os
import csv
from typing import List
from ultralytics import YOLO
from scrapping.logger import get_logger

logger = get_logger(__name__)

# -------------------------------
# CONFIG
# -------------------------------
RAW_IMAGE_DIR = "data/raw/images"
ENRICHED_DIR = "data/enriched"
OUTPUT_CSV = os.path.join(ENRICHED_DIR, "yolo_detections.csv")
YOLO_MODEL = "yolov8n.pt"  # nano model for efficiency


# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def ensure_folder(folder_path: str) -> None:
    """Ensure folder exists; create if missing."""
    try:
        os.makedirs(folder_path, exist_ok=True)
        logger.info(f"Folder ready: {folder_path}")
    except OSError as e:
        logger.exception(f"Failed to create folder: {folder_path}")
        raise


def classify_image(detected_classes: List[str]) -> str:
    """
    Classify image based on detected objects.

    Args:
        detected_classes (List[str]): List of detected object classes from YOLO.

    Returns:
        str: One of "promotional", "product_display", "lifestyle", "other"
    """
    detected_set = set(detected_classes)
    has_person = "person" in detected_set
    has_product = "bottle" in detected_set or "cell phone" in detected_set  # example proxies

    if has_person and has_product:
        return "promotional"
    elif has_product and not has_person:
        return "product_display"
    elif has_person and not has_product:
        return "lifestyle"
    else:
        return "other"


# -------------------------------
# MAIN DETECTION LOGIC
# -------------------------------
def main() -> None:
    """Run YOLO detection on all images and save results to CSV."""
    ensure_folder(ENRICHED_DIR)

    try:
        model = YOLO(YOLO_MODEL)
        logger.info(f"Loaded YOLO model: {YOLO_MODEL}")
    except Exception as e:
        logger.exception(f"Failed to load YOLO model: {YOLO_MODEL}")
        return

    csv_headers = [
        "message_id",
        "channel_name",
        "image_path",
        "detected_class",
        "confidence_score",
        "image_category",
    ]

    try:
        with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()

            if not os.path.exists(RAW_IMAGE_DIR):
                logger.warning(f"No raw images found at {RAW_IMAGE_DIR}")
                return

            for channel_name in os.listdir(RAW_IMAGE_DIR):
                channel_folder = os.path.join(RAW_IMAGE_DIR, channel_name)
                if not os.path.isdir(channel_folder):
                    continue

                for image_file in os.listdir(channel_folder):
                    if not image_file.lower().endswith((".jpg", ".jpeg", ".png")):
                        continue

                    image_path = os.path.join(channel_folder, image_file)
                    message_id = f"{channel_name}_{os.path.splitext(image_file)[0]}"

                    try:
                        results = model(image_path)
                    except Exception as e:
                        logger.exception(f"YOLO failed on {image_path}")
                        continue

                    detected_classes: List[str] = []

                    for r in results:
                        for box in r.boxes:
                            cls = model.names[int(box.cls)]
                            conf = float(box.conf)
                            detected_classes.append(cls)
                            writer.writerow({
                                "message_id": message_id,
                                "channel_name": channel_name,
                                "image_path": image_path,
                                "detected_class": cls,
                                "confidence_score": conf,
                                "image_category": "",  # placeholder
                            })

                    image_category = classify_image(detected_classes)

                    if not detected_classes:
                        writer.writerow({
                            "message_id": message_id,
                            "channel_name": channel_name,
                            "image_path": image_path,
                            "detected_class": "none",
                            "confidence_score": 0.0,
                            "image_category": image_category,
                        })

                    csvfile.flush()

    except OSError as e:
        logger.exception(f"Failed to write CSV: {OUTPUT_CSV}")
        return

    logger.info(f"YOLO detection complete! Results saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
