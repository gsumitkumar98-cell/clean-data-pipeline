# handle file path safely
from pathlib import Path
# create unique id
import uuid
from datetime import datetime

# StringIO creates an in-memory file-like object from a string
from io import StringIO

import logging
# will be using for CSV processing.
import pandas as pd
# return api errors
from fastapi import HTTPException
# clean dataframe
from src.datacleaner import clean_data
# generate summary
from src.datasummary import data_summary
import src.loggerfile
logger = logging.getLogger(__name__)
# process uploaded csv file
def process_csv(
    file_name: str,
    content: bytes
)->dict:
    
    # File size validation,max file size 5 mb
    MAX_FILE_SIZE  = 5 * 1024 * 1024

    if len(content) > MAX_FILE_SIZE :
        logger.warning(
        "File size exceeded limit for file %s",
        file_name
    )
        raise HTTPException(
            status_code=413,
            detail="File too large"
        )

       # remove unsafe path from filename
    safe_filename = Path(
        file_name
    ).name

    timestamp = datetime.now().strftime(
        "%d_%m_%y"
    )
    # create short unique id
    short_id = uuid.uuid4().hex[:6]
   
    unique_filename = (
        f"{timestamp}_{short_id}_{safe_filename}"
    )
    # raw file location
    raw_file_path = (
        f"data/raw/{unique_filename}"
    )
   # cleaned file location
    cleaned_file_path = (
        f"data/cleaned/cleaned_{unique_filename}"
    )

    # Save raw file
    with open(raw_file_path, "wb") as f:
        f.write(content)
    logger.info(
        "Raw csv file successfully saved at path %s",
        raw_file_path
    )
    # Decode file
    encodings = [
        "utf-8",
        "latin-1",
        "cp1252"
    ]

    decoded_content = None
     # try each encoding using loop
    for encoding in encodings:
        try:
            decoded_content = (
                content.decode(encoding) # converting into string
            )
            logger.info(
                "File decoded using %s encoding",
                encoding
            )
            break

        except UnicodeDecodeError:
            continue
      # if no encoding matched
    if decoded_content is None:
        logger.warning(
            "Unsupported encoding csv file found in %s",
            file_name
        )
        raise HTTPException(
            status_code=422,
            detail="Unsupported encoding"
        )

    try:
        df = pd.read_csv(
            StringIO(decoded_content)
        )
        if df.empty:
            logger.warning(
                "Empty csv file uploaded %s",
                file_name
            )
            raise HTTPException(
                status_code=400,
                detail="CSV file is empty"
            )
    # if invalid csv format found
    except pd.errors.ParserError:
        logger.warning(
        "Malformed CSV found in file %s",
        file_name
    )
        raise HTTPException(
            status_code=422,
            detail="Malformed CSV file"
        )
    #count rows before cleaning
    before_rows = len(df)
    logger.info(
    "Rows before cleaning: %s",
    before_rows
)
     # clean dataframe
    cleaned_df = clean_data(
        df,
        drop_nulls=True,
        trim_whitespace=True
    )
   # couting the rows after cleaning
    after_rows = len(cleaned_df)
    logger.info(
    "Rows after cleaning: %s",
    after_rows
)
    # save cleaned csv at cleaned file path
    cleaned_df.to_csv(
        cleaned_file_path,
        index=False
    )
    logger.info(
    "Cleaned csv file saved at %s",
    cleaned_file_path
)
     # create final summary
    summary = data_summary(
        cleaned_df
    )
    logger.info(
    "Summary generated for file %s",
    file_name
)
    logger.info(
    "Processing completed for the file %s",
    file_name
)
     # return final api json response
    return {
        "message": "File cleaned successfully",
        "raw_file": raw_file_path,
        "cleaned_file": cleaned_file_path,
        "cleaning_report": {
            "rows_before": before_rows,
            "rows_after": after_rows,
            "rows_removed": (
                before_rows - after_rows
            )
        },
        "summary": summary
    }