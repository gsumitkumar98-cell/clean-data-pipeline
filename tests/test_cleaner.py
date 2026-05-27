# pandas module
import pandas as pd

# pytest module
import pytest

# import clean_data function
from src.datacleaner import clean_data


def test_duplicate_removal():
    """
    Verify duplicate rows are removed correctly.
    """

    df = pd.DataFrame({
        "name": ["A", "A", "B"],
        "email": [
            "a@gmail.com",
            "a@gmail.com",
            "b@gmail.com"
        ]
    })

    cleaned_df = clean_data(
        df,
        remove_duplicates_enabled=True
    )

    assert len(cleaned_df) == 2


def test_trim_whitespace():
    """
    Verify leading and trailing spaces
    are removed from string columns.
    """

    df = pd.DataFrame({
        "name": [
            " Sumit ",
            " Ram "
        ]
    })

    cleaned_df = clean_data(
        df,
        trim_whitespace=True
    )

    assert cleaned_df["name"].tolist() == [
        "Sumit",
        "Ram"
    ]


def test_drop_null_rows():
    """
    Verify rows with null values
    are removed correctly.
    """

    df = pd.DataFrame({
        "name": [
            "Sumit",
            None
        ]
    })

    cleaned_df = clean_data(
        df,
        drop_nulls=True
    )

    assert len(cleaned_df) == 1


def test_invalid_dataframe():
    """
    Verify invalid dataframe input
    raises TypeError.
    """

    with pytest.raises(TypeError):

        clean_data("invalid dataframe")


def test_invalid_duplicate_subset():
    """
    Verify invalid subset columns
    raise ValueError.
    """

    df = pd.DataFrame({
        "name": ["A"]
    })

    with pytest.raises(ValueError):

        clean_data(
            df,
            remove_duplicates_enabled=True,
            duplicate_subset=["salary"]
        )


def test_invalid_trim_flag():
    """
    Verify invalid trim_whitespace
    flag raises TypeError.
    """

    df = pd.DataFrame()

    with pytest.raises(TypeError):

        clean_data(
            df,
            trim_whitespace="yes"
        )


def test_empty_dataframe():
    """
    Verify empty dataframe
    returns safely.
    """

    df = pd.DataFrame()

    cleaned_df = clean_data(df)

    assert cleaned_df.empty


def test_original_dataframe_not_modified():
    """
    Verify original dataframe
    is not mutated during cleaning.
    """

    df = pd.DataFrame({
        "name": [" Sumit "]
    })

    original_df = df.copy()

    clean_data(
        df,
        trim_whitespace=True
    )

    assert df.equals(original_df)