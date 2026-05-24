# Creates the API application. UploadFile Handles uploaded files. File Tells FastAPI that the parameter should come from a file upload.
from fastapi import FastAPI, UploadFile, File
# Handle cors
from fastapi.middleware.cors import CORSMiddleware
# will be using for CSV processing.
import pandas as pd
# StringIO creates an in-memory file-like object from a string
from io import StringIO
# using for file and folder operations.
import os
#import of data cleaning funtion
from src.datacleaner import clean_data
# import of data loading function
from src.datasummary import data_summary


# Create a FastAPI application instance with API metadata for Swagger documentation
app = FastAPI(
    title="Clean Data Pipeline API",
    description="API for cleaning CSV files and generating summaries",
    version="1.0.0"
)

#cors configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #any frontend can access api
    allow_credentials=True, 
    allow_methods=["*"], # all http headers are allowed
    allow_headers=["*"] # all request headers are allowed
)

#creating the raw folder
os.makedirs("data/raw", exist_ok=True)

#creating the folder for store cleaned data
os.makedirs("data/cleaned", exist_ok=True)

@app.get("/")
def home():
    return {
       "message":"clean data pipeline api is running"
    }

# api for upload and clean csv file.
@app.post("/summary")
async def upload_csv(
    file: UploadFile=File(...) # required file
):
    try:
        # validation for check file extension
        if not file.filename.endswith(".csv"):
            return{
               "error":"only csv file is allowed"
            }
        #Read the uploaded file  as bytes.
        content = await file.read()

        #store raw file 
        raw_file_path = (
            f"data/raw/{file.filename}"
        )

        # open and write the file
        with open(raw_file_path, "wb") as f:
            f.write(content)
       
        # decode content from bytes
        decoded_content = content.decode("utf-8")

        #used StringIO for convert content into file obj
        decoded_file= StringIO(decoded_content)
        #generating the dataframe
        df=pd.read_csv(decoded_file)
      
        #storing original cound of dataframe before cleaning 
        before_rows = len(df)
       
        #call the cleaning function
        cleaned_df=clean_data(df,drop_nulls=True,trim_whitespace=True)

        #dataframe count after cleaning
        after_rows=len(cleaned_df)

        #save cleaned file path
        cleaned_file_path=(f"data/cleaned/cleaned_{file.filename}")
        
        #convert cleaned dataframe into csv
        cleaned_df.to_csv(
            cleaned_file_path,
            index=False,  #Avoids saving row numbers.
        )

        #generate summary
        summary=data_summary(cleaned_df)
        return{
            "message":("file cleaned successfully"),
            "raw file":raw_file_path,
            "cleaned file":cleaned_file_path,
            "cleaning report":{
                "rows before cleaning":before_rows,
                "row after cleaning":after_rows,
                "rows removed after cleaning":(before_rows-after_rows)
            },
            "summary":summary
        }
    except Exception as e:
        return {
            "error": str(e)
        }

