import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"


def get_logger(name="motor_insurance_analytics"):
    """Create and return a configured logger."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


logger = get_logger()


def log_pipeline_step(step_name, message=None):
    """Log a pipeline step."""
    if message is None:
        logger.info("%s", step_name)
    else:
        logger.info("%s: %s", step_name, message)


def log_error(message, error=None):
    """Log an error message and optional exception."""
    if error is not None:
        logger.error("%s: %s", message, error)
    else:
        logger.error("%s", message)