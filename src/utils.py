import pandas as pd

# helper function for remove or trim the extraspaces
def trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    # selected all dataframe columns with datatype and select only string(object)
    object_columns = df.select_dtypes(
        include=["object"]
    ).columns
    #loop over the coloumns and remove spaces using strip() method
    for col in object_columns:
        df[col] = df[col].str.strip()

    return df

# helper function for  remove the dublicate using dataframe with subset list or non subset
def remove_duplicates(df: pd.DataFrame,subset: list[str] | None = None) -> pd.DataFrame:
    return df.drop_duplicates(subset=subset)

#helper function for remove null values
def drop_null_rows(
    df: pd.DataFrame
) -> pd.DataFrame:
    return df.dropna()