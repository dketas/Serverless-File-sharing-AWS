import json
import boto3
import base64
import logging
import os

# Initialize the S3, SES, and Cognito clients
s3 = boto3.client('s3')
ses = boto3.client('ses')
cognito_client = boto3.client('cognito-idp')

# Bucket and Sender Email
BUCKET_NAME = 'sfss-bucket'  # Your S3 bucket name
SENDER_EMAIL = 'ketandhamane9856@gmail.com'  # Replace with your SES verified email
USER_POOL_ID = 'eu-west-1_ruh2fQmWE'  # Replace with your Cognito User Pool ID

def lambda_handler(event, context):
    try:
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
        
        # Upload the file to S3
        params = {
            'Bucket': BUCKET_NAME,
            'Key': file_name,
            'Body': body,
            'ContentType': content_type
        }
        s3.put_object(**params)
        # Generate the download link
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
        # Get the user's email address from Cognito
        user_id = event['requestContext']['authorizer']['claims']['sub']  # Cognito User ID (sub)
        user_email = get_user_email_from_cognito(user_id)
        # Send email notification using SES
        subject = "File Uploaded Successfully"
        body_html = f"""
        <html>
        <head></head>
        <body>
          <h1>File Uploaded Successfully</h1>
          <p>Your file <b>{file_name}</b> has been uploaded successfully.</p>
          <p>You can download it using the link below:</p>
          <a href="{file_url}" target="_blank">{file_url}</a>
        </body>
        </html>
        """
        ses.send_email(
            Source=SENDER_EMAIL,
            Destination={"ToAddresses": [user_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Html": {"Data": body_html}}
            }
        )
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "File uploaded and email sent successfully",
                "downloadLink": file_url
            })
        }
    except Exception as e:
        logging.error(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error uploading file or sending email", "error": str(e)})
        }

# Helper function to get the user's email from Cognito
def get_user_email_from_cognito(user_id):
    try:
        # Get the user information from Cognito
        response = cognito_client.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=user_id
        )
        
        # Find the email attribute in the user's attributes
        for attribute in response['UserAttributes']:
            if attribute['Name'] == 'email':
                return attribute['Value']
        raise Exception("Email attribute not found for user.")
    
    except Exception as e:
        logging.error(f"Error fetching user email from Cognito: {str(e)}")
        raise

