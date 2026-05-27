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
    duplicate_subset: list[str] | None = None,
    remove_duplicates_enabled: bool = False,
    
) -> pd.DataFrame:
    """
    Clean and transform a pandas DataFrame
    using configurable cleaning operations.

    The function applies optional whitespace trimming,
    null row removal, and duplicate removal while
    returning a cleaned dataframe copy without
    modifying the original dataframe.

    Parameters:
        df (pd.DataFrame):
            Input dataframe.

        drop_nulls (bool):
            Remove rows containing null values.

        trim_whitespace (bool):
            Remove leading and trailing spaces
            from string columns.

        remove_duplicates_enabled (bool):
            Enable duplicate row removal.

        duplicate_subset (list[str] | None):
            Columns used for duplicate checking.

    Returns:
        pd.DataFrame:
            Cleaned dataframe after applying
            selected transformations.

    Raises:
        TypeError:
            If invalid parameter types are provided.

        ValueError:
            If any cleaning operation fails.
    """
    if not isinstance(drop_nulls, bool):
        raise TypeError(
            "drop_nulls must be boolean"
        )
    
    if not isinstance(trim_whitespace, bool):
        raise TypeError(
            "trim_whitespace must be boolean"
        )

    if not isinstance( remove_duplicates_enabled, bool ):
        raise TypeError(
                "remove_duplicates_enabled must be boolean"
            )
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "df must be a pandas DataFrame"
        )
    if duplicate_subset is not None:
        if not all( isinstance(col, str)for col in duplicate_subset):
            raise TypeError(
                "All subset columns must be strings"
            )
    cleaned_df = df.copy()
    
    before_rows = len(df)

    logger.info(
        f"Rows before cleaning: {before_rows}"
    )
    
    if trim_whitespace:
        try:    
            logger.info(
                "Started whitespace trimming"
            )
            cleaned_df = trim_whitespace_func(
            cleaned_df
            )
            logger.info(
            "Whitespace trimming completed"
            )
        except Exception as e:
            logger.exception(
                "Error while trimming whitespaces"
            )

            raise ValueError(
                f"Whitespace cleaning failed: {str(e)}"
            )
        
    
    if drop_nulls:
        try:
            before_null_drop = len(cleaned_df)

            cleaned_df = drop_null_rows(
                cleaned_df
            )
            removed_null_rows = (
                before_null_drop - len(cleaned_df)
            )
            logger.info(
                "Rows removed after null cleaning: %s",
                removed_null_rows
            )

        except Exception as e:
            logger.exception(
                "Error while removing null rows"
            )
            raise ValueError(
                f"Null cleaning failed: {str(e)}"
            )
        
    if remove_duplicates_enabled:
        try:
            before_duplicate_removal = len(
                cleaned_df
            )
            # performing removing dublicates operation if it is true in args based on subset
            cleaned_df = remove_duplicates(
                cleaned_df,
                subset=duplicate_subset
            )
            removed_duplicate_rows = (
                before_duplicate_removal
                - len(cleaned_df)
            )
            logger.info(
                "Duplicate rows removed: %s",
                removed_duplicate_rows
            )
        except Exception as e:
            logger.exception(
                "Error while removing duplicate rows"
            )
            raise ValueError(
                f"Duplicate removal failed: {str(e)}"
            )
        
    #checking after cleaning length of dataframe
    after_rows = len(cleaned_df)

    logger.info(
        "Cleaning completed successfully. Rows before: %s, Rows after: %s",
        before_rows,
        after_rows
    )

    return cleaned_df