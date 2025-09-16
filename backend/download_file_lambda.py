import json
import boto3
import logging
import base64

# Initialize the S3 client
s3 = boto3.client('s3')
BUCKET_NAME = 'sfss-bucket'  # Your S3 bucket name

def lambda_handler(event, context):
    try:
        # Extract the file name from query parameters
        file_name = event['queryStringParameters']['fileName']
        
        # Retrieve the file from S3
        params = {
            'Bucket': BUCKET_NAME,
            'Key': file_name
        }
        
        # Get the object from S3
        response = s3.get_object(**params)
        
        # Read the file content and encode it to base64
        file_content = base64.b64encode(response['Body'].read()).decode('utf-8')
        return {
            'statusCode': 200,
            'body': file_content,
            'isBase64Encoded': True,
            'headers': {
                'Content-Disposition': f'attachment; filename="{file_name}"'
            }
        }
    except Exception as error:
        logging.error(f"Error downloading file: {error}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error downloading file', 'error': str(error)})
        }

