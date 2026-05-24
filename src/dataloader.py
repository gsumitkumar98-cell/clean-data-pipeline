import pandas as pd
# raised when the CSV file exists but contains no data.
from pandas.errors import EmptyDataError, ParserError

# use for load csv file with file path args and return dataframe
def load_csv(path: str) -> pd.DataFrame:
 
    try:
        #reading the csv using path
        df = pd.read_csv(path)
        return df
    # exception handling done
    except FileNotFoundError:
        raise FileNotFoundError(
            f"ERROR: File not found -> {path}"
        )

    except EmptyDataError:
        raise ValueError(
            "ERROR: CSV file is empty"
        )

    except ParserError:
        raise ValueError(
            "ERROR: Invalid CSV format"
        )

    except Exception as e:
        raise Exception(
            f"Unexpected error while loading CSV: {str(e)}"
        )