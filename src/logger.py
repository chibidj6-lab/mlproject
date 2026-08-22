import logging
import os
from datetime import datetime

# Define log file naming convention with current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create a logs directory inside the current working directory
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE) 
#logs is the folder name and LOG_FILE is the file name. os.getcwd() will give the current working directory.
os.makedirs(logs_path, exist_ok=True) 
#exist_ok=True will not raise an error if the folder already exists. It will just ignore the error and continue with the code execution.

# Full path for the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure the logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Optional: Add StreamHandler to simultaneously output logs to VS Code Terminal
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(
#     logging.Formatter("[ %(asctime)s ] %(levelname)s - %(message)s")
# )
# logging.getLogger().addHandler(console_handler)

# To run the program and check if the logging is working fine