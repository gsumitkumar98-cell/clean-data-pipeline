# default python logger module
import logging

# handle file paths safely
from pathlib import Path
from os import PathLike

# pandas module
import pandas as pd

# pandas csv exceptions
from pandas.errors import (
    EmptyDataError,
    ParserError
)

logger = logging.getLogger(__name__)


def load_csv(
    path: str | PathLike,
    encoding: str = "utf-8",
    delimiter: str = ","
) -> pd.DataFrame:
    """
    Load CSV file into pandas dataframe.

    Parameters:
        path (str | PathLike):
            CSV file path.

        encoding (str):
            File encoding type.

        delimiter (str):
            CSV delimiter character.

    Returns:
        pd.DataFrame:
            Loaded dataframe.

    Raises:
        TypeError:
            If path is invalid.

        FileNotFoundError:
            If file does not exist.

        ValueError:
            If file is empty or malformed.

        RuntimeError:
            If unexpected loading error occurs.
    """

    try:

        # validate path type
        if not isinstance(
            path,
            (str, PathLike)
        ):

            raise TypeError(
                "path must be string or PathLike object"
            )

        # convert path safely
        file_path = Path(path)

        # validate empty path
        if not str(file_path).strip():

            raise ValueError(
                "CSV file path cannot be empty"
            )

        # validate file extension
        if file_path.suffix.lower() != ".csv":

            raise ValueError(
                "Only CSV files are supported"
            )

        logger.info(
            "Started loading csv file: %s",
            file_path
        )

        # load csv dataframe
        df = pd.read_csv(
            file_path,
            encoding=encoding,
            sep=delimiter
        )

        logger.info(
            "CSV loaded successfully with %s rows and %s columns",
            len(df),
            len(df.columns)
        )

        return df

    except FileNotFoundError:

        logger.exception(
            "CSV file not found: %s",
            path
        )

        raise FileNotFoundError(
            f"File not found: {path}"
        )

    except EmptyDataError:

        logger.exception(
            "CSV file is empty: %s",
            path
        )

        raise ValueError(
            "CSV file is empty"
        )

    except ParserError:

        logger.exception(
            "Invalid CSV format found in file: %s",
            path
        )

        raise ValueError(
            "Invalid CSV format"
        )

    except TypeError:
        raise

    except ValueError:
        raise

    except Exception as e:

        logger.exception(
            "Unexpected error while loading csv file: %s",
            path
        )

        raise RuntimeError(
            f"Unexpected csv loading error: {str(e)}"
        )