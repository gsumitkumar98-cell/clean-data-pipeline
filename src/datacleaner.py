# default logger module for python
import logging
# import of python module
import pandas as pd
# import of all the utils helper functions 
from src.utils import (
    trim_whitespace as trim_whitespace_func,
    remove_duplicates,
    drop_null_rows
)

logger = logging.getLogger(__name__)

# clean data function 
def clean_data(
    df: pd.DataFrame,
    drop_nulls: bool = False,
    trim_whitespace: bool = False,
    duplicate_subset: list[str] | None = None
) -> pd.DataFrame:
    #before cleaning calculate length of dataframe
    before_rows = len(df)

    logger.info(
        f"Rows before cleaning: {before_rows}"
    )
    # performing trim whitespace operation if it is true in args
    if trim_whitespace:
        df = trim_whitespace_func(df)
    # performing null removing operation if it is true in args
    if drop_nulls:
        df = drop_null_rows(df)
    # performing removing dublicates operation if it is true in args based on subset
    df = remove_duplicates(
        df,
        subset=duplicate_subset
    )
    #checking after cleaning length of dataframe
    after_rows = len(df)

    logger.info(
        f"Rows after cleaning: {after_rows}"
    )

    return df