import os

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate_oauth(scopes=None):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # Todo: Make token.json and credentials.json functino arguments
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials2.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def authenticate_service_account(scopes=None):
    service_account_info = {
        "type": "service_account",
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv("CLIENT_CERT_URL")
    }
    return service_account.Credentials.from_service_account_info(service_account_info, scopes=scopes)


def authenticate() -> Credentials:
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    # Todo: Use oauth in debug?
    return authenticate_service_account(scopes)
