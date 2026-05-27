# Creates the API application. UploadFile Handles uploaded files. File Tells FastAPI that the parameter should come from a file upload.
from fastapi import FastAPI, UploadFile, File, HTTPException
# Handle cors
from fastapi.middleware.cors import CORSMiddleware

# using for file and folder operations.
import os
import src.loggerfile
import logging
from pydantic import BaseModel

from src.services.csv_service import process_csv

class CleaningReport(BaseModel):
    rows_before: int
    rows_after: int
    rows_removed: int

class SummaryResponse(BaseModel):
    message: str
    raw_file: str
    cleaned_file: str
    cleaning_report: CleaningReport
    summary: dict

# Create a FastAPI application instance with API metadata for Swagger documentation
app = FastAPI(
    title="Clean Data Pipeline API",
    description="API for cleaning CSV files and generating summaries",
    version="1.0.0"
)

#cors configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], #any frontend can access api
    allow_credentials=True, 
    allow_methods=["*"], # all http headers are allowed
    allow_headers=["*"] # all request headers are allowed
)

#creating the raw folder
os.makedirs("data/raw", exist_ok=True)

#creating the folder for store cleaned data
os.makedirs("data/cleaned", exist_ok=True)

logger = logging.getLogger(__name__)

@app.get("/")
def home():
    return {
       "message":"clean data pipeline api is running"
    }

# api for upload and clean csv file.
@app.post("/summary",response_model=SummaryResponse)
async def upload_csv(
    file: UploadFile = File(...)
):

    try:
        logger.info(
            "Started processing file %s",
            file.filename
        )
        ALLOWED_CONTENT_TYPES = [
            "text/csv",
            "application/vnd.ms-excel"
        ]

        if file.content_type not in ALLOWED_CONTENT_TYPES:

            logger.warning(
                "Invalid content type uploaded: %s",
                file.content_type
            )

            raise HTTPException(
                status_code=400,
                detail="Invalid file type"
            )
                        #check  validation for the file extension.
        if not file.filename.lower().endswith(
            ".csv"
        ):
            logger.info(
            "Found enexpected file type uploaded: %s",
            file.filename
        )
            raise HTTPException(
                status_code=400,
                detail="Only CSV files allowed"
            )

        content = await file.read()
        
       #process csv for the data cleaning
        result = process_csv(
            file.filename,
            content
        )
        # return the summary json response
        return result

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
        "Unexpected error while processing file %s",
        file.filename
    )
        raise HTTPException(
            status_code=500,
            # detail="Internal server error"
            detail=str(e)
        )
