from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import re
import json
import time
from google.auth.transport.requests import Request
import base64


# Set the API scope and credentials file
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CLIENT_SECRET_FILE = 'client_secret_73901197763-9gt2575g7emibf0v4mehgp2fjsf59q3i.apps.googleusercontent.com.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
TOKEN_FILE = 'token.json'


def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail service
    service = build(API_NAME, API_VERSION, credentials=creds)
    return service


def extract_otp_from_email_body(encoded_body):
    decoded_body = base64.urlsafe_b64decode(encoded_body).decode('utf-8')
    print(decoded_body)
    # Now you can search for the OTP pattern in the decoded body
    otp_match = re.search(r'\b\d{6}\b', decoded_body)
    if otp_match:
        return otp_match.group(0)

    print('No OTP found in the email.')
    return None


def get_otp_from_email(service, user_id='me', subject='Unacademy: Login-OTP'):
    try:
        # Get the list of messages matching the subject
        response = service.users().messages().list(
            userId=user_id, q=f'subject:{subject}').execute()
        messages = response.get('messages', [])

        if not messages:
            print('No messages found with the specified subject.')
            return None

        # Get the latest message
        latest_message_id = messages[0]['id']
        message = service.users().messages().get(
            userId=user_id, id=latest_message_id).execute()

        # Iterate through the parts in the message
        for part in message['payload']['parts']:
            # Check if 'body' key exists in the part
            if 'body' in part:
                # Extract the encoded body from the 'body' key
                encoded_body = part['body']['data']
                # Extract OTP from the decoded body
                otp = extract_otp_from_email_body(encoded_body)
                if otp:
                    return otp

        return None

        # # Extract OTP from the message body using regex
        # match = re.search(r'\b\d{6}\b', message['snippet'])
        # print("............")
        # out_file = open("myfile.json", "w")
        # json.dump(message, out_file, indent=4)
        # out_file.close()
        # print("............")
        # if match:
        #     return match.group()
        # else:
        #     print('No OTP found in the email.')
        #     return None

    except Exception as e:
        print(f'An error occurred: {e}')
        return None


if __name__ == '__main__':
    service = get_gmail_service()

    while True:
        # Poll for new emails every 60 seconds
        time.sleep(5)

        # Get OTP from the latest email
        otp = get_otp_from_email(service)
        if otp:
            print(f'OTP found: {otp}')
            break
