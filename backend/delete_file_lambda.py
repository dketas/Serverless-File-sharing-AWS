import json
import boto3
import logging

# Initialize the S3 client
s3 = boto3.client('s3')
BUCKET_NAME = 'sfss-bucket'  # Your S3 bucket name

def lambda_handler(event, context):
    try:
        # Extract the file name from query parameters
        file_name = event.get('queryStringParameters', {}).get('fileName')
        if not file_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing fileName query parameter"})
            }

        # Delete the file from S3
        s3.delete_object(Bucket=BUCKET_NAME, Key=file_name)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"File '{file_name}' deleted successfully"})
        }

    except Exception as error:
        logging.error(f"Error deleting file: {error}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error deleting file", "error": str(error)})
        }

