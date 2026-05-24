# clean-data-pipeline

I have created CSV Cleaning Backend API for csv file. via this api endpoint you will be
able to upload the csv and clean your csv.

Project flow will be, user upload csv file -> fastapi will get csv file -> load csv using pandas -> pass csv through the cleaning funcion -> generate the summary -> save the cleaned csv file -> return json response of api call.


Project folder breakdown:

# 1. api/app.py
Creates the API application. UploadFile Handles uploaded files. File Tells FastAPI that the parameter should come from a file upload.
** from fastapi import FastAPI, UploadFile, File**

# Handle cors
** from fastapi.middleware.cors import CORSMiddleware ** 

# will be using for CSV processing.
** import pandas as pd ** 

# StringIO is used to treat a string as a file object in memory.
** from io import StringIO ** 
Normally, functions like pandas.read_csv() expect a file. If your data is already in a string, StringIO creates a file-like object so those functions can read it.
Example: 
from io import StringIO
import pandas as pd

csv_data = """name,age
Sumit,25
Rahul,30
"""

file_like_object = StringIO(csv_data)

df = pd.read_csv(file_like_object)

print(df)

# used fastapi with metadata for Swagger documentation
# done cors configurations
# created folders for raw and cleaned data
# created API endpoints 
@app.get("/") 
for check app is working
@app.post("/summary")
Handles the complete CSV processing pipeline:
- Accepts a CSV file upload.
- Validates the uploaded file.
- Creates folders for storing raw and cleaned files.
- Saves the original CSV file.
- Loads the CSV into a Pandas DataFrame.
- Cleans the data using the `clean_data()` function.
- Generates dataset statistics using the `data_summary()` function.
- Saves the cleaned CSV file.
- Returns a JSON response containing file paths, cleaning report, and summary information.


# 2. src/datacleaner.py
    Cleans and preprocesses a DataFrame.
    Trims whitespace from string columns (trim_whitespace=True).
    Removes rows with null values (drop_nulls=True).
    Removes duplicate rows.
    Supports duplicate removal based on specific columns (duplicate_subset).
    Logs row count before cleaning.
    Logs row count after cleaning.
    Returns the cleaned DataFrame.
# 3. src/dataloader.py
    Loads a CSV file into a Pandas DataFrame.
    Reads the CSV using pd.read_csv().
    Returns the loaded DataFrame.
    Handles missing file errors (FileNotFoundError).
    Handles empty CSV files (EmptyDataError).
    Handles invalid CSV format errors (ParserError).
    Provides user-friendly error messages.
    Catches and reports unexpected exceptions.

# 4. src/datasummary.py
    Generates summary statistics for a DataFrame.
    Returns the summary as a dictionary.
    Calculates total number of rows.
    Calculates total number of columns.
    Calculates missing values for each column.
    Calculates total duplicate rows.
    Identifies data types of all columns.
    Provides a quick overview of dataset quality and structure.

# 5. loggerfile.py
    Configures application logging.
    Creates a logs directory if it does not exist.
    Stores log messages in logs/app.log.
    Sets logging level to INFO.
    Records log timestamp, log level, and message.
    Helps track application activity and errors.
    Useful for debugging and monitoring the application.



# 6. tests/test_cleaner.py
    1. Import pandas
    2. Import clean_data function
    3. Create test function
    4. Create data with 2 identical rows
    5. Convert data into DataFrame
    6. Call clean_data()
    7. clean_data() removes duplicates
    8. Check remaining row count
    9. Test passes if count == 1
     10. Test fails with AssertionError if count != 1

# 7. tests/test_loader.py
     flow of test_load_csv_success():
        1. Call load_csv("tests/sample.csv")
        2. CSV file is found
        3. Data is loaded into a DataFrame
        4. Check number of rows using len(df)
        5. Assert that row count is greater than 0
        6. Test passes if CSV contains data

     Flow of test_load_csv_missing_file()
        1. Enter pytest.raises(FileNotFoundError) block
        2. Call load_csv("missing.csv")
        3. load_csv raises FileNotFoundError
        4. pytest catches the exception
        5. Test passes because the expected exception occurred

# 8. tests/test_summary.py
       1. Creates a sample DataFrame with test data.
       2. Calls the data_summary() function.
       3. Verifies that the summary contains the "rows" key.
       4. Verifies that the summary contains the "columns" key.
       5. Verifies that the summary contains the "missing_values" key.
       6. Ensures the summary output follows the expected structure.
       7. Fails if any required summary field is missing.

# 9. tests/test_main.py
  Test 1: test_main_cli_success()
        Creates a temporary CSV file with sample data.
        Runs the CLI application using subprocess.run().
        Verifies that the command executes successfully.
        Verifies that the output CSV file is created.
        Parses the JSON summary returned by the application.
        Confirms that the summary contains:
        rows
        columns
        missing_values
        Ensures the end-to-end CLI workflow works correctly.

  Test 2: test_main_missing_file()
        Runs the CLI application with a non-existent input file.
        Verifies that the application exits with an error.
        Confirms that a "File not found" message is displayed.
        Ensures proper error handling for invalid file paths.


