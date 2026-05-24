import pandas as pd
# Import the clean_data function that we want to test
from src.datacleaner import clean_data

# Test function to verify duplicate rows are removed
def test_duplicate_removal():

    data = {
        "name": ["A", "A"], # Duplicate names
        "email": ["x@gmail.com", "x@gmail.com"]  # Duplicate emails
    }
    # Convert the dictionary into a Pandas DataFrame
    df = pd.DataFrame(data)
    # Pass the DataFrame to the cleaning function
    cleaned = clean_data(df)
    # used assert for verifying if after remove duplicate length should be 1
    assert len(cleaned) == 1