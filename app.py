from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
import requests
import json
import os
from datetime import datetime
from database import backup_database
from foalder import create_archive

import logging

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)
# log the start of new run
logging.info('------------------------- New run at %s -------------------------', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Your account_id and application_key
account_id = os.environ.get('BACKBLAZE_ACCOUNT_ID')
application_key = os.environ.get('BACKBLAZE_KEY')
bucket_id = os.environ.get('BACKBLAZE_BUCKET_ID')
print(account_id, application_key, bucket_id)

try:
    response = requests.get(
        'https://api.backblazeb2.com/b2api/v3/b2_authorize_account',
        auth=(account_id, application_key)
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    logging.error(f"HTTP error occurred: {err}")
except Exception as err:
    logging.error(f"An error occurred: {err}")
else:
    response_json = response.json()
    auth_token = response_json['authorizationToken']
    api_url = response_json['apiInfo']['storageApi']['apiUrl'] + '/b2api/v3'
    logging.info("Successfully got authorization token.")


# Get upload URL
response = requests.post(
    api_url + '/b2_get_upload_url',
    headers={'Authorization': auth_token},
    json={'bucketId': bucket_id} 
)

response_json = response.json()

upload_url = response_json['uploadUrl']
upload_auth_token = response_json['authorizationToken']


file_path = create_archive()

# Open the file in binary mode
with open(file_path, 'rb') as f:
    file_content = f.read()

# Upload file
headers = {
    'Authorization': upload_auth_token,
    'X-Bz-File-Name': os.path.basename(file_path),
    'Content-Type': 'application/zip',
    'X-Bz-Content-Sha1': 'do_not_verify'
}

# Upload file
try:
    response = requests.post(
        upload_url,
        headers=headers,
        data=file_content
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    logging.error(f"HTTP error occurred: {err}")
except Exception as err:
    logging.error(f"An error occurred: {err}")
else:
    logging.info("File uploaded successfully.")
    os.remove(file_path)
    logging.info(f"Deleted local file: {file_path}")

# create the sql backup
sql_file_path = backup_database()

# open the slq file in binary mode
with open(sql_file_path, 'rb') as f:
    sql_file_content = f.read()

headers_sql = {
    'Authorization': upload_auth_token,
    'X-Bz-File-Name': os.path.basename(sql_file_path),
    'Content-Type': 'application/sql',
    'X-Bz-Content-Sha1': 'do_not_verify'
}
# Upload SQL file
try:
    response = requests.post(
        upload_url,
        headers=headers_sql,
        data=sql_file_content
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    logging.error(f"HTTP error occurred: {err}")
except Exception as err:
    logging.error(f"An error occurred: {err}")
else:
    logging.info("SQL file uploaded successfully.")
    os.remove(sql_file_path)
    logging.info(f"Deleted local SQL file: {sql_file_path}")