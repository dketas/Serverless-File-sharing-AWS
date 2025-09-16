import json
import boto3
import logging

# Initialize the S3 client
s3 = boto3.client('s3')
BUCKET_NAME = 'sfss-bucket'  # Your S3 bucket name

def lambda_handler(event, context):
    try:
        # List objects in the specified S3 bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        # Check if the bucket is empty
        if 'Contents' not in response:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "No files found"})
            }
        # Extract file names from the response
        files = [{"name": file['Key']} for file in response['Contents']]
        return {
            "statusCode": 200,
            "body": json.dumps({"files": files})
        }
    except Exception as error:
        logging.error(f"Error listing files: {error}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error listing files", "error": str(error)})
        }

