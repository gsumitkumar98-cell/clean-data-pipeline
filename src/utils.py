import pandas as pd

# helper function for remove or trim the extraspaces
def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove leading and trailing spaces
    from dataframe string columns.

    Parameters:
        df (pd.DataFrame):
            Input dataframe.

    Returns:
        pd.DataFrame:
            Cleaned dataframe with
            trimmed string values.

    Raises:
        TypeError:
            If input is not a pandas DataFrame.

        ValueError:
            If whitespace cleaning fails.
    """
    try:
        if not isinstance(df,pd.DataFrame):
           raise TypeError(
                "df must be a pandas DataFrame"
            )

        if df.empty:
            return df.copy()
        # Create a dataframe copy
        cleaned_df = df.copy()
        # selected all dataframe columns with datatype and select only string(object)
        object_columns = cleaned_df.select_dtypes(
                include=["object","string"]
            ).columns
        #loop over the coloumns and remove spaces using strip() method
        for col in object_columns:
            # cleaned_df[col] = cleaned_df[col].str.strip()
            cleaned_df[col] = cleaned_df[col].apply(
                lambda value:
                value.strip()
                if isinstance(value,str)
                else value
            )

        return cleaned_df
    except Exception as e:
                raise ValueError(
                    f"Error while removing whitespaces: {str(e)}"
                )

# helper function for  remove the dublicate using dataframe with subset list or non subset
def remove_duplicates(df: pd.DataFrame,subset: list[str] | None = None) -> pd.DataFrame:
    """
    Remove duplicate rows from dataframe.

    Parameters:
        df (pd.DataFrame):
            Input dataframe.

        subset (list[str] | None):
            Column names used for
            duplicate checking.

    Returns:
        pd.DataFrame:
            Dataframe after removing
            duplicate rows.

    Raises:
        TypeError:
            If input is not a pandas DataFrame.

        ValueError:
            If invalid columns are provided
            or duplicate removal fails.
    """
    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError(
                "df must be a pandas DataFrame"
            )
        if subset is not None:
            invalid_columns=[
                col
                for col in subset
                if col not in df.columns
            ]
            if invalid_columns:
                raise ValueError(
                    f"invalid columns found: {invalid_columns}"
                )
        return df.drop_duplicates(subset=subset)
    except Exception as e:
            raise ValueError(
                f"Error while removing duplicate rows: {str(e)}"
            )


#helper function for remove null values
def drop_null_rows(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Remove rows containing null values.

    Parameters:
        df (pd.DataFrame):
            Input dataframe.

    Returns:
        pd.DataFrame:
            Dataframe after removing null rows.

    Raises:
        TypeError:
            If input is not a pandas DataFrame.
    """
    try:
        if not isinstance(df,pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")
        return df.dropna()
    except Exception as e:
        raise ValueError(
            f"Error while dropping null rows: {str(e)}"
        )