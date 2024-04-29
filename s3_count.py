import boto3
from datetime import datetime
import os
import re

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket name and key from event
    bucket = event['detail']['requestParameters']['bucketName']
    key = event['detail']['requestParameters']['key']

    # Check if the file is in the /out folder and is a .txt file
    if not key.startswith('out/') or not key.endswith('.txt'):
        return {
            'statusCode': 200,
            'body': 'File is not in the /out folder or is not a .txt file'
        }

    # Download the file from S3
    local_file_path = '/tmp/' + os.path.basename(key)
    s3.download_file(bucket, key, local_file_path)

    # Count words in the file
    with open(local_file_path, 'r') as file:
        content = file.read()
        word_count = len(re.findall(r'\w+', content))

    # Append count to file name and add execution date and time details
    new_filename = f"{os.path.splitext(os.path.basename(key))[0]}_{word_count}_count.txt"
    execution_details = f"Execution Date: {datetime.now().strftime('%Y-%m-%d')}, Execution Time: {datetime.now().strftime('%H:%M:%S')}"
    new_content = f"File Name: {os.path.basename(key)}, Word Count: {word_count}, {execution_details}"

    # Upload the count.txt file back to S3
    s3.put_object(Bucket=bucket, Key=f'out/{new_filename}', Body=new_content)

    return {
        'statusCode': 200,
        'body': 'Word count appended to file name and uploaded to S3'
    }
