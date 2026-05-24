#default python module for packaging 
import logging
# using for file and folder operations.example for create or read or delete file.
import os

os.makedirs("logs", exist_ok=True)

# logger configurations
logging.basicConfig(
    level=logging.INFO,
    filename="logs/app.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)