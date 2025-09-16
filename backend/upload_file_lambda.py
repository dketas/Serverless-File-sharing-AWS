import json
import boto3
import base64
import logging
import os

# Initialize the S3 client
s3 = boto3.client('s3')
BUCKET_NAME = 'sfss-bucket'  # Your S3 bucket name

def lambda_handler(event, context):
    try:
        # Log the incoming event for debugging
        logging.info(f"Received event: {json.dumps(event)}")
        # Extract fileName and contentType from query parameters or headers
        file_name = event.get('queryStringParameters', {}).get('fileName')
        content_type = event.get('headers', {}).get('Content-Type', 'application/octet-stream')
        
        if not file_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Missing fileName query parameter"})
            }
        # Decode the request body if it's base64-encoded
        body = event.get('body', '')
        if event.get('isBase64Encoded', False):
            body = base64.b64decode(body)
        # Log the body for debugging
        logging.info(f"Body decoded: {body[:100]}...")  # Only log first 100 bytes to avoid large logs
        # Prepare the parameters for uploading the file to S3
        params = {
            'Bucket': BUCKET_NAME,
            'Key': file_name,
            'Body': body,
            'ContentType': content_type
        }
        # Upload the file to S3
        s3.put_object(**params)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "File uploaded successfully"})
        }
    except Exception as error:
        logging.error(f"Error uploading file: {error}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error uploading file", "error": str(error)})
        }

