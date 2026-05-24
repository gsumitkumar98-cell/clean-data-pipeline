import pandas as pd
from src.datasummary import data_summary

# Import the data_summary function that we want to test
def test_summary_output():
    # Created a sample DataFrames
    df = pd.DataFrame({
        "name": ["A", "B"],
        "age": [20, 30]
    })
    # Generate summary  from the DataFrame
    summary = data_summary(df)
     # Verify that the summary contains a "rows","column" and "missing_values" keys
    assert "rows" in summary
    assert "columns" in summary
    assert "missing_values" in summary