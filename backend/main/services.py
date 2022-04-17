from decouple import config

from datetime import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authorize_and_build_service():
    creds = None
    if os.path.exists(config('CREDENTIALS_FOLDER') + 'token.json'):
        creds = Credentials.from_authorized_user_file(config('CREDENTIALS_FOLDER') + 'token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config('CREDENTIALS_FOLDER') + 'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(config('CREDENTIALS_FOLDER') + 'token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except HttpError as error:
        print('An error occurred: %s' % error)
