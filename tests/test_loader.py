# pathlib module for safe file paths
from pathlib import Path

# pytest module
import pytest

# pandas module
import pandas as pd

# import loader function
from src.dataloader import load_csv


def test_load_csv_success(tmp_path):
    """
    Verify valid CSV file loads successfully.
    """

    sample_file = tmp_path / "sample.csv"

    sample_file.write_text(
        "name,email\n"
        "Sumit,sumit@gmail.com\n"
        "Ram,ram@gmail.com"
    )

    df = load_csv(sample_file)

    assert isinstance(df, pd.DataFrame)

    assert len(df) == 2

    assert list(df.columns) == [
        "name",
        "email"
    ]


def test_load_csv_missing_file():
    """
    Verify missing file raises FileNotFoundError.
    """

    with pytest.raises(FileNotFoundError):

        load_csv("missing.csv")


def test_load_csv_empty_file(tmp_path):
    """
    Verify empty CSV file raises ValueError.
    """

    empty_file = tmp_path / "empty.csv"

    empty_file.write_text("")

    with pytest.raises(ValueError):

        load_csv(empty_file)


def test_load_csv_invalid_extension(tmp_path):
    """
    Verify non-csv files raise ValueError.
    """

    text_file = tmp_path / "sample.txt"

    text_file.write_text(
        "invalid content"
    )

    with pytest.raises(ValueError):

        load_csv(text_file)


def test_load_csv_invalid_input_type():
    """
    Verify invalid path type raises TypeError.
    """

    with pytest.raises(TypeError):

        load_csv(123)


def test_load_csv_malformed_csv(tmp_path):
    """
    Verify malformed CSV raises ValueError.
    """

    malformed_file = (
        tmp_path / "bad.csv"
    )

    malformed_file.write_text(
        'name,email\n'
        '"Sumit,sumit@gmail.com'
    )

    with pytest.raises(ValueError):

        load_csv(malformed_file)


def test_load_csv_custom_delimiter(
    tmp_path
):
    """
    Verify CSV loads correctly
    using custom delimiter.
    """

    sample_file = (
        tmp_path / "semicolon.csv"
    )

    sample_file.write_text(
        "name;email\n"
        "Sumit;sumit@gmail.com"
    )

    df = load_csv(
        sample_file,
        delimiter=";"
    )

    assert len(df) == 1

    assert list(df.columns) == [
        "name",
        "email"
    ]


def test_load_csv_preserves_data(
    tmp_path
):
    """
    Verify loaded dataframe
    preserves expected values.
    """

    sample_file = (
        tmp_path / "users.csv"
    )

    sample_file.write_text(
        "name,age\n"
        "Sumit,25\n"
        "Ram,30"
    )

    df = load_csv(sample_file)

    assert df.iloc[0]["name"] == "Sumit"

    assert df.iloc[1]["age"] == 30