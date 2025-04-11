import os 
import logging 
# from from_root import from_root 
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Constants for log configuration
LOG_DIR = 'logs'
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Number of backup log files to keep



log_dir_path = os.path.join(os.getcwd(),LOG_DIR)
os.makedirs(log_dir_path,exist_ok=True)
log_file_path = os.path.join(log_dir_path,LOG_FILE)

def configure_logger():
  """
  Configuring Logger with rotating File handler and console handler 
  """
  
  # Create a custom logger class 
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)
  
  # Defining Formatter
  formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s") 
  
  # File handler with rotation 
  # logging and RotatingFileHandler: These come from Python’s built‑in logging module. They let you create log messages and manage log files that automatically “rotate” (i.e. create a new file) once they reach a set size.
  
  #   This sets up a handler that writes log messages to the file specified by log_file_path.
  # It will automatically create a new log file when the current file exceeds 5 MB.
  # It keeps up to 3 old log files as backups
  file_handler = RotatingFileHandler(log_file_path,maxBytes=MAX_LOG_SIZE,backupCount=BACKUP_COUNT)
  
  file_handler.setFormatter(formatter)
  file_handler.setLevel(logging.DEBUG)
  
  # Console Handlers 
  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)
  console_handler.setLevel(logging.INFO)
  
  # Add handlers to Logger 
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)
  
configure_logger()
  



