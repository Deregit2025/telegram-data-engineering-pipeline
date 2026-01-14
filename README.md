
# Telegram Medical Data Scraper

**Project:** Week 8 Challenge – Shipping a Data Product  
**Objective:** Extract messages and images from public Telegram channels related to Ethiopian medical products and store them in a raw data lake for further processing.  

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Folder Structure](#folder-structure)  
- [Setup](#setup)  
- [Configuration](#configuration)  
- [Running the Scraper](#running-the-scraper)  
- [Security](#security)  
- [Logging](#logging)  
- [Dependencies](#dependencies)  

---

## Overview

This project implements **Task 1: Data Scraping and Collection** from the Week 8 Challenge.  

- Scrapes public Telegram channels (e.g., CheMed, Lobelia Cosmetics, Tikvah Pharma)  
- Downloads message data and images  
- Stores raw JSON messages in `data/raw/messages`  
- Organizes images in `data/raw/images/{channel_name}/{message_id}.jpg`  
- Logs scraping activity in `logs/scraper.log`  

The output serves as the foundation for downstream tasks like DBT transformations, YOLO image enrichment, and analytical API development.

---

## Features

- Scrapes **message ID, text, date, views, forwards, and media info**  
- Downloads images from messages containing photos  
- Configurable channels and storage paths via YAML config  
- Logging of errors, progress, and channels scraped  

---

## Folder Structure

```

medical-telegram-warehouse/
├── config/
│   └── scraping_config.yaml
├── data/
│   ├── raw/
│   │   ├── messages/
│   │   └── images/
├── logs/
├── src/
│   └── scraping/
│       ├── scrapper.py
│       ├── telegram_client.py
│       └── image_downloader.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md

````

---

## Setup

1. Clone the repo:  
```bash
git clone <repo-url>
cd medical-telegram-warehouse
````

2. Create a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows PowerShell
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

1. Create a `.env` file in the root directory with your Telegram API credentials:

```
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_NAME=telegram_scraper_session
```

2. Update `config/scraping_config.yaml` for channels and storage paths:

```yaml
telegram:
  channels:
    - chemed
    - lobelia4cosmetics
    - tikvahpharma

storage:
  raw_message_path: data/raw/messages
  raw_images_path: data/raw/images

logging:
  logs_path: logs/scraper.log
```

---

## Running the Scraper

```bash
python -m src.scraping.scrapper
```

* On first run, you will be prompted for **phone number**, **OTP code**, and **Telegram 2FA password** (if enabled).
* Session file will be saved automatically and reused on subsequent runs.

---

## Security

**Do NOT commit `.env` or session files** to GitHub. Exposing `API_ID`, `API_HASH`, or `.session` can lead to your Telegram account being hacked or banned.

Add these to `.gitignore`:

```
.env
*.session
```

---

## Logging

* All activity is logged to the file specified in `scraping_config.yaml`
* Logs include errors, channels scraped, and scraping progress

---

## Dependencies

* `Telethon` – Telegram client for Python
* `PyYAML` – YAML configuration handling
* `python-dotenv` – Load environment variables from `.env`
* Standard Python libraries: `asyncio`, `logging`, `os`, `json`

---

## Next Steps

* Task 2: Load scraped data into PostgreSQL and build DBT transformations
* Task 3: Enrich data using YOLO object detection on images
* Task 4: Expose cleaned data via FastAPI
* Task 5: Orchestrate the full pipeline with Dagster


