import subprocess
import os
from dagster import op

@op
def run_dbt_transformations():
    dbt_project_dir = os.path.abspath("dbt/medical_warehouse")

    if not os.path.exists(dbt_project_dir):
        raise Exception(f"dbt project directory not found: {dbt_project_dir}")

    result = subprocess.run(
        ["dbt", "run"],
        cwd=dbt_project_dir,     
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(
            "dbt run failed\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    print(result.stdout)
