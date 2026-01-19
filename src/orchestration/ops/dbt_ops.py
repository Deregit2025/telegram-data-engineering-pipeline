"""
Dagster op for running dbt transformations.

This module defines a Dagster operation (`op`) that executes dbt models
inside the `dbt/medical_warehouse` project. It captures and logs output,
and raises exceptions if the dbt run fails.
"""

import subprocess
import os
from typing import Optional
from dagster import op
from scrapping.logger import get_logger

logger = get_logger(__name__)


@op
def run_dbt_transformations(dbt_project_dir: Optional[str] = None) -> None:
    """
    Run dbt transformations for the medical_warehouse project.

    Args:
        dbt_project_dir (str, optional): Absolute or relative path to the dbt project.
            Defaults to 'dbt/medical_warehouse'.

    Raises:
        FileNotFoundError: If the dbt project directory does not exist.
        RuntimeError: If the dbt run command fails.
    """
    if dbt_project_dir is None:
        dbt_project_dir = os.path.abspath("dbt/medical_warehouse")

    if not os.path.exists(dbt_project_dir):
        logger.error(f"dbt project directory not found: {dbt_project_dir}")
        raise FileNotFoundError(f"dbt project directory not found: {dbt_project_dir}")

    logger.info(f"Starting dbt run in: {dbt_project_dir}")

    try:
        result = subprocess.run(
            ["dbt", "run"],
            cwd=dbt_project_dir,
            capture_output=True,
            text=True,
            check=True  # raises CalledProcessError on non-zero exit
        )
        logger.info("dbt run completed successfully.")
        logger.info(f"dbt STDOUT:\n{result.stdout}")
        if result.stderr:
            logger.warning(f"dbt STDERR:\n{result.stderr}")

    except subprocess.CalledProcessError as e:
        logger.exception(
            f"dbt run failed with return code {e.returncode}\n"
            f"STDOUT:\n{e.stdout}\n"
            f"STDERR:\n{e.stderr}"
        )
        raise RuntimeError(f"dbt run failed. See logs for details.") from e
    except Exception as e:
        logger.exception("Unexpected error while running dbt transformations.")
        raise
