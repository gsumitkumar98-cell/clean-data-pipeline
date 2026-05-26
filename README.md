# Clean Data Pipeline API

A FastAPI-based backend application for uploading, validating, cleaning, and summarizing CSV files.

The API accepts a CSV file, performs validation checks, cleans the dataset, generates summary statistics, stores both raw and cleaned files, and returns a structured JSON response.

---

## Features

- CSV file upload
- MIME type validation
- File extension validation
- File size validation (5 MB limit)
- Filename sanitization
- Path traversal protection
- Multiple encoding support
  - UTF-8
  - Latin-1
  - CP1252
- Empty CSV validation
- Malformed CSV detection
- Duplicate row removal
- Null value removal
- Whitespace trimming
- Dataset summary generation
- Structured logging
- Swagger API documentation
- Automated testing with Pytest

---

## Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| FastAPI | API Framework |
| Pandas | CSV Processing |
| NumPy | Data Operations |
| Uvicorn | ASGI Server |
| Pydantic | Data Validation |
| Pytest | Automated Testing |

---

## Project Structure

```text
clean-data-pipeline/
│
├── api/
│   └── app.py
│
├── src/
│   ├── datacleaner.py
│   ├── datasummary.py
│   ├── loggerfile.py
│   │
│   └── services/
│       └── csv_service.py
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── logs/
│   └── app.log
│
├── tests/
│   ├── test_cleaner.py
│   ├── test_loader.py
│   ├── test_summary.py
│   └── test_main.py
│
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Application Flow

```text
Client Upload CSV
        |
        v
FastAPI Endpoint
        |
        v
Validate File
        |
        v
Save Raw File
        |
        v
Decode Content
        |
        v
Create DataFrame
        |
        v
Clean Data
        |
        v
Generate Summary
        |
        v
Save Cleaned CSV
        |
        v
Return JSON Response
```

---

## Validation Rules

The API performs multiple validation checks before processing the file.

### File Validation

- Only `.csv` files are allowed
- MIME type validation
- Maximum file size: 5 MB

### Security Validation

- Filename sanitization using `Path(file_name).name`
- Unique file naming using timestamp and UUID
- Protection against path traversal attacks

### CSV Validation

- Empty CSV detection
- Malformed CSV detection
- Encoding validation

---

## Supported Encodings

The API supports the following encodings:

```text
utf-8
latin-1
cp1252
```

The service automatically attempts each encoding until one succeeds.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/gsumitkumar98-cell/clean-data-pipeline.git

cd clean-data-pipeline
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### Install Runtime Dependencies

```bash
pip install -r requirements.txt
```

---

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

---

## Python Version

Developed and tested with:

```text
Python 3.11+
```

---

## Running the Application

Start the FastAPI server:

```bash
uvicorn api.app:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Health Check

#### Request

```http
GET /
```

#### Response

```json
{
  "message": "clean data pipeline api is running"
}
```

---

### Upload and Clean CSV

#### Request

```http
POST /summary
```

Content-Type:

```text
multipart/form-data
```

Parameter:

| Name | Type | Required |
|--------|--------|--------|
| file | CSV File | Yes |

---

## Success Response

```json
{
  "message": "File cleaned successfully",
  "raw_file": "data/raw/25_05_26_ab12cd_orders.csv",
  "cleaned_file": "data/cleaned/cleaned_25_05_26_ab12cd_orders.csv",
  "cleaning_report": {
    "rows_before": 100,
    "rows_after": 95,
    "rows_removed": 5
  },
  "summary": {
    "rows": 95,
    "columns": 8,
    "missing_values": {},
    "duplicate_rows": 0
  }
}
```

---

## Error Responses

### Invalid File Type

```http
400 Bad Request
```

```json
{
  "detail": "Only CSV files allowed"
}
```

---

### Invalid MIME Type

```http
400 Bad Request
```

```json
{
  "detail": "Invalid file type"
}
```

---

### Empty CSV

```http
400 Bad Request
```

```json
{
  "detail": "CSV file is empty"
}
```

---

### File Too Large

```http
413 Payload Too Large
```

```json
{
  "detail": "File too large"
}
```

---

### Unsupported Encoding

```http
422 Unprocessable Entity
```

```json
{
  "detail": "Unsupported encoding"
}
```

---

### Malformed CSV

```http
422 Unprocessable Entity
```

```json
{
  "detail": "Malformed CSV file"
}
```

---

### Internal Server Error

```http
500 Internal Server Error
```

```json
{
  "detail": "Internal server error"
}
```

---

## Logging

Application logs are stored in:

```text
logs/app.log
```

Logged events include:

- File upload
- Validation failures
- Encoding detection
- CSV parsing
- Data cleaning
- Summary generation
- Unexpected exceptions

Example:

```text
2026-05-27 22:30:01 - INFO - Started processing file orders.csv
2026-05-27 22:30:02 - INFO - File decoded using utf-8 encoding
2026-05-27 22:30:03 - INFO - Processing completed for the file orders.csv
```

---

## Testing

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src
```

### Covered Scenarios

- Valid CSV upload
- Invalid file extension
- Invalid MIME type
- File size validation
- Empty CSV
- Unsupported encoding
- Malformed CSV
- Duplicate removal
- Summary generation

---

## Design Decisions

### Why Service Layer?

Business logic is separated from API routes.

```text
app.py
    |
    ---> csv_service.py
              |
              ---> clean_data()
              ---> data_summary()
```

Benefits:

- Better maintainability
- Easier testing
- Clear separation of concerns
- Cleaner API layer

---

## Future Improvements

- Docker support
- AWS S3 integration
- Background task processing
- Async file handling
- Authentication and authorization
- Database integration
- Environment-based configuration management

---

## Author

**Sumit Kumar Gupta**

Python Backend Developer

Technologies:
- Python
- FastAPI
- Pandas
- REST APIs
- Data Processing
- Pytest