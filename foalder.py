from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import os
import time
import logging
from datetime import datetime
import shutil

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)

def create_archive():
    # Your directory path
    dir_path = os.environ.get('DIR_PATH')

    # Get current date
    current_date = datetime.now().strftime('%Y%m%d%H%M%S')

    # Record the start time
    start_time = time.time()

    # Create a zip file (archive)
    file_path = shutil.make_archive(f'{current_date}', 'zip', dir_path)

    # Record the end time
    end_time = time.time()

    # Calculate the time taken
    time_taken = end_time - start_time

    # Calculate the compression rate
    original_size = get_dir_size(dir_path)
    compressed_size = os.path.getsize(file_path)
    compression_rate = original_size / compressed_size

    # Log the results
    logging.info(f"Archive created: {file_path}. Time taken: {time_taken} seconds. Compression rate: {compression_rate}.")

    return file_path

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total