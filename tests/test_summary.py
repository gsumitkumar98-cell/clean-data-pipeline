# pandas module
import pandas as pd

# pytest module
import pytest

# import summary function
from src.datasummary import data_summary


def test_summary_output():
    """
    Verify summary contains
    correct dataframe statistics.
    """

    df = pd.DataFrame({
        "name": ["A", "B"],
        "age": [20, 30]
    })

    summary = data_summary(df)

    assert summary["rows"] == 2

    assert summary["columns"] == 2

    assert summary["duplicate_rows"] == 0

    assert summary["missing_values"] == {
        "name": 0,
        "age": 0
    }

    assert summary["column_types"] == {
        "name": "object",
        "age": "int64"
    }


def test_summary_missing_values():
    """
    Verify missing values
    are calculated correctly.
    """

    df = pd.DataFrame({
        "name": ["A", None],
        "age": [20, None]
    })

    summary = data_summary(df)

    assert summary["missing_values"] == {
        "name": 1,
        "age": 1
    }


def test_summary_duplicate_rows():
    """
    Verify duplicate rows
    are counted correctly.
    """

    df = pd.DataFrame({
        "name": ["A", "A"],
        "age": [20, 20]
    })

    summary = data_summary(df)

    assert summary["duplicate_rows"] == 1


@pytest.mark.parametrize(
    "dataframe, expected_rows",
    [
        (
            pd.DataFrame({
                "name": ["A"]
            }),
            1
        ),
        (
            pd.DataFrame({
                "name": ["A", "B", "C"]
            }),
            3
        )
    ]
)
def test_summary_row_counts(
    dataframe,
    expected_rows
):
    """
    Verify row counts
    using parametrized inputs.
    """

    summary = data_summary(
        dataframe
    )

    assert summary["rows"] == expected_rows


def test_summary_empty_dataframe():
    """
    Verify empty dataframe
    summary generation works safely.
    """

    df = pd.DataFrame()

    summary = data_summary(df)

    assert summary["rows"] == 0

    assert summary["columns"] == 0


def test_summary_invalid_input():
    """
    Verify invalid input
    raises TypeError.
    """

    with pytest.raises(TypeError):

        data_summary("invalid")


def test_summary_numeric_statistics():
    """
    Verify numeric statistics
    are generated correctly.
    """

    df = pd.DataFrame({
        "salary": [1000, 2000, 3000]
    })

    summary = data_summary(df)

    assert "numeric_summary" in summary

    assert (
        summary["numeric_summary"]
        ["salary"]["mean"]
        == 2000.0
    )


def test_summary_unique_values():
    """
    Verify unique value counts
    are generated correctly.
    """

    df = pd.DataFrame({
        "city": [
            "Delhi",
            "Delhi",
            "Mumbai"
        ]
    })

    summary = data_summary(df)

    assert summary["unique_values"] == {
        "city": 2
    }