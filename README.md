

# Telegram Medical Data Warehouse & Analytics Pipeline

**Project:** Week 8 Challenge – Shipping a Data Product
**Objective:** Extract, transform, enrich, and analyze data from Ethiopian medical-related Telegram channels in a fully automated pipeline.

---

## Table of Contents

* [Overview](#overview)
* [Tasks](#tasks)

  * [Task 1 – Data Scraping](#task-1---data-scraping)
  * [Task 2 – Data Modeling & DBT Transformations](#task-2---data-modeling--dbt-transformations)
  * [Task 3 – Image Enrichment with YOLO](#task-3---image-enrichment-with-yolo)
  * [Task 4 – Analytical API with FastAPI](#task-4---analytical-api-with-fastapi)
  * [Task 5 – Pipeline Orchestration with Dagster](#task-5---pipeline-orchestration-with-dagster)
* [Folder Structure](#folder-structure)
* [Setup & Installation](#setup--installation)
* [Configuration](#configuration)
* [Running the Pipeline](#running-the-pipeline)
* [Security](#security)
* [Logging](#logging)
* [Dependencies](#dependencies)
* [Next Steps & Recommendations](#next-steps--recommendations)

---

## Overview

This project implements a full **end-to-end data pipeline** for Telegram channels:

1. **Task 1:** Scrape messages and images
2. **Task 2:** Load data into a **PostgreSQL warehouse** and transform using **dbt** (with star schema design)
3. **Task 3:** Enrich images using **YOLOv8 object detection**
4. **Task 4:** Expose analytical endpoints via **FastAPI REST API**
5. **Task 5:** Orchestrate the pipeline using **Dagster** for automation and monitoring

The pipeline supports **data-driven insights**, including channel activity, post trends, visual content analysis, and product popularity.

---

## Tasks

### Task 1 – Data Scraping

**Objective:** Collect messages and images from public Telegram channels.

**Key Steps:**

* Scrape message metadata: ID, text, date, views, forwards, media info
* Download images and store in structured directories
* Store raw JSON messages in a **data lake**
* Logging of progress and errors

**Scripts:**

* `src/scraping/scrapper.py` – main scraping script
* `src/scraping/telegram_client.py` – Telegram client setup
* `src/scraping/image_downloader.py` – downloads media

**Outputs:**

* `data/raw/messages/` – JSON messages
* `data/raw/images/{channel_name}/{message_id}.jpg` – images

---

### Task 2 – Data Modeling & DBT Transformations

**Objective:** Transform raw data into a structured data warehouse using **dbt**, following a **star schema**.

**Key Steps:**

* Create staging tables to clean and normalize data
* Build **fact** and **dimension tables** for analytics:

| Table          | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| `fct_messages` | Fact table with message metrics (views, forwards, media flags) |
| `dim_channels` | Channel details and stats                                      |
| `dim_dates`    | Calendar dimensions (day, week, month, year, weekend)          |

* Implement dbt **models** and **tests** for data quality
* Star schema enables efficient aggregation and analytics

**Outputs:**

* Populated warehouse tables: `fct_messages`, `dim_channels`, `dim_dates`
* DBT models and documentation

---

### Task 3 – Image Enrichment with YOLO

**Objective:** Analyze images using **YOLOv8** to extract analytical insights.

**Key Steps:**

* Run object detection on images downloaded in Task 1
* Record detected objects with confidence scores
* Classify images into categories:

| Category        | Criteria         |
| --------------- | ---------------- |
| promotional     | Person + product |
| product_display | Product only     |
| lifestyle       | Person only      |
| other           | Neither detected |

* Integrate results into a warehouse table `fct_image_detections`

**Scripts:**

* `src/yolo/yolo_detect.py` – YOLO detection script

**Outputs:**

* `data/enriched/fct_image_detections.csv`
* Enriched warehouse table linked to `fct_messages`

---

### Task 4 – Analytical API with FastAPI

**Objective:** Expose warehouse and YOLO-enriched data via a REST API.

**Key Endpoints:**

| Endpoint                                    | Description                          |
| ------------------------------------------- | ------------------------------------ |
| GET `/api/reports/top-products`             | Returns top mentioned products       |
| GET `/api/channels/{channel_name}/activity` | Returns channel posting trends       |
| GET `/api/search/messages`                  | Search messages by keyword           |
| GET `/api/reports/visual-content`           | Visual content statistics by channel |

**Scripts:**

* `api/main.py` – API entry point
* `api/schemas.py` – Pydantic request/response validation
* `api/database.py` – Database connection via SQLAlchemy

**Outputs:**

* API documentation via OpenAPI at `/docs`
* Endpoint responses for analytical queries

---

### Task 5 – Pipeline Orchestration with Dagster

**Objective:** Automate and schedule the full pipeline for reliability.

**Key Steps:**

* Convert pipeline into **Dagster jobs and ops**:

1. `scrape_telegram_data`
2. `load_raw_to_postgres`
3. `run_dbt_transformations`
4. `run_yolo_enrichment`

* Define execution order and dependencies
* Launch Dagster UI for monitoring
* Schedule daily runs with alerts

**Scripts:**

* `src/dagster_pipeline/pipeline.py` – pipeline definition

**Outputs:**

* Automated pipeline with logging and error handling
* Schedulable daily execution with observability

---

## Folder Structure

```
medical-telegram-warehouse/
├── api/                     # FastAPI API
├── config/                  # Scraping and DB config
├── data/                    # Raw, enriched, warehouse data
├── logs/                    # Pipeline and scraper logs
├── notebooks/               # Exploratory analysis and visualizations
├── src/
│   ├── scraping/            # Task 1
│   ├── yolo/                # Task 3
│   └── dagster_pipeline/    # Task 5
├── dbt/                     # Task 2: dbt models
├── .env
├── requirements.txt
└── README.md
```

---

## Setup & Installation

```bash
git clone <repo-url>
cd medical-telegram-warehouse
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

---

## Configuration

* `.env` – Telegram credentials and database connection
* `config/scraping_config.yaml` – channels and paths

---

## Security

* Do NOT commit `.env` or `.session` files
* Add to `.gitignore`:

```
.env
*.session
```

---

## Logging

* Scraper logs
* DBT transformation logs
* YOLO enrichment logs
* API and pipeline execution logs
* Stored in `logs/`

---

## Dependencies

* **Scraping:** Telethon, PyYAML, python-dotenv
* **DBT & Database:** dbt, psycopg2
* **Image Enrichment:** ultralytics, OpenCV
* **API:** FastAPI, SQLAlchemy, Pydantic, Uvicorn
* **Orchestration:** Dagster
* **Standard:** asyncio, logging, os, json, pandas

---

## Next Steps & Recommendations

* Fine-tune YOLO for **medical product detection**
* Add more Telegram channels for richer insights
* Build dashboards using **notebooks/ or BI tools**
* Implement sentiment analysis for text messages
* Monitor pipeline metrics and failures via Dagster UI



