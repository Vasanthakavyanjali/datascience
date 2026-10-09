
from pathlib import Path

from src.data_loader import load_all_data
from src.validation import validate_all_data
from src.data_cleaner import clean_data, save_cleaned_data
from src.insurance_analysis import calculate_kpis
from src.logger import get_logger


PROJECT_ROOT = Path(__file__).resolve().parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
CLEANED_DATA_DIR = PROJECT_ROOT / "data" / "cleaned"

logger = get_logger(__name__)


def main():
    logger.info("Motor Insurance Analytics pipeline started.")

    try:
        logger.info("Loading raw datasets.")
        data = load_all_data(data_dir=RAW_DATA_DIR)

        logger.info("Validating datasets.")
        validation_errors = validate_all_data(data)

        if validation_errors:
            for error in validation_errors:
                logger.error(str(error))

            raise ValueError(
                "Data validation failed. Review the errors in the log."
            )

        logger.info("Cleaning datasets.")
        cleaned_data = clean_data(data)

        logger.info("Saving cleaned datasets.")
        save_cleaned_data(
            cleaned_data,
            output_dir=CLEANED_DATA_DIR,
        )

        logger.info("Calculating insurance KPIs.")
        kpis = calculate_kpis(cleaned_data)

        print("\nMotor Insurance Analytics KPIs")
        print("-" * 40)

        for name, value in kpis.items():
            print(f"{name}: {value}")

        logger.info("Pipeline completed successfully.")

    except Exception:
        logger.exception("Pipeline failed.")
        raise


if __name__ == "__main__":
    main()