"""
Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""
import datetime

import dotenv

from bva.src.google_sheets.service import get_technicians_for_date

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1nNVrzcVQFULWVans5zt3N0_tqsl6U9U1hzGV_mhseJ4'
SAMPLE_RANGE_NAME = 'Turnus Våren 2022!A1:C'

dotenv.load_dotenv()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("date", type=datetime.date.fromisoformat)
    args = parser.parse_args()

    technician = get_technicians_for_date(args.date)
    print(technician)
