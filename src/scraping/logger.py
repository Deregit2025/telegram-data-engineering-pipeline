import logging
from pathlib import Path


def setup_logger(log_file: str):
    """
    Configure logging for the scraping pipeline.
    Logs are written to file and stdout.
    """
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )
