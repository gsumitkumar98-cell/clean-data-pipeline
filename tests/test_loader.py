import pytest
# Import the load_csv function that we want to test
from src.dataloader import load_csv

# Test case to verify that a valid CSV file loads 
def test_load_csv_success():
     # testing with load sample CSV file from the tests folder
    df = load_csv("tests/sample.csv")
     # checking if length of dataframe should be atleast 1
    assert len(df) > 0

# Test case to verify when the file does not exist
def test_load_csv_missing_file():
     # Check that the code inside this block raises a FileNotFoundError
    with pytest.raises(FileNotFoundError):
         # Try loading a file that does not exist
        load_csv("missing.csv")