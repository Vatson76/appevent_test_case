import os.path
import logging

from decouple import config

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.conf import settings

from company.models import Company

logger = logging.getLogger('backend.main.services')
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authorize_and_build_service(company: Company):
    logger.debug('Authorization to google API')
    if settings.DEBUG:
        path = config('CREDENTIALS_FOLDER')
    else:
        path = config('CREDENTIALS_FOLDER') + 'company{}/'.format(company.id)
    creds = None
    if os.path.exists(path + 'token.json'):
        logger.info('Using existing credentials to authorize')

        creds = Credentials.from_authorized_user_file(path + 'token.json', SCOPES)
    if not creds or not creds.valid:
        logger.warning('Requesting new credetials')

        if creds and creds.expired and creds.refresh_token:
            logger.info('Refreshing token')

            creds.refresh(Request())
        else:
            logger.info('Getting new token')
            flow = InstalledAppFlow.from_client_secrets_file(
                path + 'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(path + 'token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        logger.debug('Successfully authorized')

        return service
    except HttpError as error:
        logger.exception('An error occurred: %s' % error)
