import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .auth import authenticate


def read_spreadsheet(spreadsheet_id: str, range):
    creds = authenticate()
    try:
        service = build('sheets', 'v4', credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range).execute()
        values = result.get('values', [])

        if not values:
            logging.warning(f"No data found in spreadsheet {spreadsheet_id}, range {range}")

        return values
    except HttpError as err:
        logging.error(err)