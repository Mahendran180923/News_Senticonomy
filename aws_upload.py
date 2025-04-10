import os
import json
import boto3
from botocore.exceptions import ClientError

# file_size = os.path.getsize('news_data.csv')

# if file_size < 1024:
#     print(f"The size of the CSV file is: {file_size} bytes")
# elif file_size < 1024 ** 2:
#     print(f"The size of the CSV file is: {file_size / 1024:.2f} KB")
# else:
#     print(f"The size of the CSV file is: {file_size / (1024 ** 2):.2f} MB")

# Output: The size of the CSV file is: 325.68 MB


# Load secrets from secrets.json
with open('.vscode/secrets.json') as f:
    secrets = json.load(f)



# Security Credentials


access_key = secrets['AWS_ACCESS_KEY']
secret_key = secrets['AWS_SECRET_KEY']

# Connect with AWS S3 Client
s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
    )


file = "raw_data.csv"
try:
    s3_client.upload_file(file, 'senticonomy', 'raw_data.csv')
    print(f"File {file} uploaded successfully to S3 bucket 'senticonomy'")
except ClientError as e:
    print(f"Error uploading file {file} to S3 bucket 'senticonomy': {e}")
