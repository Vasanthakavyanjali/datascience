
from pathlib import Path
import pandas as pd

from src.logger import log_pipeline_step, log_error

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

REQUIRED_FILES = {
    "customers": "customers.csv",
    "vehicles": "vehicles.csv",
    "policies": "policies.csv",
    "claims": "claims.csv",
    "payments": "payments.csv",
}


def load_csv(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()
        log_pipeline_step(
            f"Loaded {file_path.name}: {len(df)} rows"
        )
        return df
    except Exception as exc:
        log_error(f"Failed to load {file_path}: {exc}")
        raise


def load_all_data(data_dir=None):
    directory = (
        Path(data_dir) if data_dir is not None
        else RAW_DATA_DIR
    )

    missing_files = [
        filename
        for filename in REQUIRED_FILES.values()
        if not (directory / filename).is_file()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Missing required CSV files in "
            f"{directory}: {', '.join(missing_files)}"
        )

    data = {}

    for table_name, filename in REQUIRED_FILES.items():
        data[table_name] = load_csv(directory / filename)

    log_pipeline_step("All five CSV files loaded successfully")
    return data