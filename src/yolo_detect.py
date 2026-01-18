# src/yolo_detect.py

import os
import csv
from ultralytics import YOLO

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
def ensure_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

def classify_image(detected_classes):
    """Classify image based on detected objects"""
    detected_classes = set(detected_classes)
    has_person = 'person' in detected_classes
    has_product = 'bottle' in detected_classes or 'cell phone' in detected_classes  # example product proxies

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
def main():
    ensure_folder(ENRICHED_DIR)

    # Load YOLOv8 model
    model = YOLO(YOLO_MODEL)

    # Prepare CSV
    csv_headers = ["message_id", "channel_name", "image_path", "detected_class", "confidence_score", "image_category"]

    with open(OUTPUT_CSV, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()

        # Walk through all channel folders
        for channel_name in os.listdir(RAW_IMAGE_DIR):
            channel_folder = os.path.join(RAW_IMAGE_DIR, channel_name)
            if not os.path.isdir(channel_folder):
                continue

            for image_file in os.listdir(channel_folder):
                if not image_file.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue

                image_path = os.path.join(channel_folder, image_file)
                message_id = f"{channel_name}_{image_file.split('.')[0]}"

                # Run YOLO detection
                results = model(image_path)

                detected_classes = []
                for r in results:
                    for box in r.boxes:
                        cls = model.names[int(box.cls)]
                        conf = float(box.conf)
                        detected_classes.append(cls)
                        # Write one row per detected object
                        writer.writerow({
                            "message_id": message_id,
                            "channel_name": channel_name,
                            "image_path": image_path,
                            "detected_class": cls,
                            "confidence_score": conf,
                            "image_category": ""  # placeholder, will fill later
                        })

                # Classify image
                image_category = classify_image(detected_classes)
                
                # Update CSV rows with image_category
                # For simplicity, append category as a new row if no object detected
                if not detected_classes:
                    writer.writerow({
                        "message_id": message_id,
                        "channel_name": channel_name,
                        "image_path": image_path,
                        "detected_class": "none",
                        "confidence_score": 0.0,
                        "image_category": image_category
                    })
                else:
                    # Normally, YOLO may detect multiple objects; update last N rows
                    # Simple approach: add category for each detected object row
                    csvfile.flush()  # ensure data is written

    print(f"YOLO detection complete! Results saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
