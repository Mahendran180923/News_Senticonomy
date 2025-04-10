import json
import boto3
from botocore.exceptions import ClientError


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


s3_client.download_file('senticonomy', 'raw_data.csv', 'uncleaned_data.csv')  #(Bucket name, File Name, Downloading Path)