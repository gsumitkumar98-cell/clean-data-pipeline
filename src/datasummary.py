import pandas as pd

# function for generate summary dictionary for given dataframe
def data_summary(df: pd.DataFrame) -> dict:
    
    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),

        "missing_values": (
            df.isnull().sum().to_dict()
        ),

        "duplicate_rows": int(
            df.duplicated().sum()
        ),

        "column_types": {
            col: str(dtype)
            for col, dtype in df.dtypes.items()
        }
    }

    return summary