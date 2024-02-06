from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
import logging
from datetime import datetime
from sys import platform
import time

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

def backup_database():
    # Your database credentials
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    # Get current timestamp
    current_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Set the backup file path
    backup_file_path = f'{current_timestamp}.sql'

    # Set the path to mysqldump
    # Replace these paths with the actual paths on your systems
    mysqldump_path_win = '"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe"'
    if platform == "win32":
        mysqldump_path = mysqldump_path_win
    else:
        mysqldump_path ="mysqldump"

    
    # Create a backup with mysqldump
    command = f'{mysqldump_path} -u {db_user} -p{db_password} {db_name} > {backup_file_path}'

    # Execute the command
    try:
        # Record the start time
        start_time = time.time()
        os.system(command)
        # Record the end time
        end_time = time.time()
         # Calculate the time taken
        time_taken = end_time - start_time
        logging.info(f"SQL backup created: {backup_file_path}. Time taken: {time_taken} seconds.")
    except Exception as e:
        logging.error(f"Failed to create backup: {e}")

    # Return the backup file path
    return backup_file_path