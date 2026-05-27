# default python logger module
import logging

# handle file paths safely
from pathlib import Path


def setup_logger() -> logging.Logger:
    """
    Configure and return application logger.

    Returns:
        logging.Logger:
            Configured application logger.

    Raises:
        RuntimeError:
            If logger setup fails.
    """

    try:

        # create logs directory safely
        log_directory = Path("logs")

        log_directory.mkdir(
            exist_ok=True
        )

        # log file path
        log_file_path = (
            log_directory / "app.log"
        )

        # create named logger
        logger = logging.getLogger(
            "clean_data_pipeline"
        )

        # avoid duplicate handlers
        if logger.handlers:
            return logger

        logger.setLevel(logging.INFO)

        # file log handler
        file_handler = logging.FileHandler(
            log_file_path,
            encoding="utf-8"
        )

        # log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - "
            "%(levelname)s - %(message)s"
        )

        file_handler.setFormatter(
            formatter
        )

        # add handler into logger
        logger.addHandler(
            file_handler
        )

        logger.info(
            "Logger configured successfully"
        )

        return logger

    except Exception as e:

        raise RuntimeError(
            f"Logger setup failed: {str(e)}"
        )