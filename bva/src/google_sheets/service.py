import datetime
import logging
import typing

from .sheets import read_spreadsheet

log = logging.getLogger("bva")


def get_technicians_for_date(date: datetime.date) -> typing.Optional[typing.Dict[str, str]]:
    spreadshet_id = "1nNVrzcVQFULWVans5zt3N0_tqsl6U9U1hzGV_mhseJ4"
    schedule_range = "A2:C"
    info_range = "E2:F13"

    schedule_rows = read_spreadsheet(spreadshet_id, schedule_range)
    info_rows = read_spreadsheet(spreadshet_id, info_range)
    # Todo: Put model somewhere else
    technicians = {"PC": None, "Lyd": None}

    def find_info(name):
        for row in info_rows:
            if not row:
                continue
            first, last = row
            if first is None or last is None:
                continue
            if first == name:
                return f"{first} {last}"

    for row in schedule_rows:
        if not row:
            continue
        value_date = datetime.datetime.strptime(row[0], "%d. %B %Y").date()
        if value_date == date:
            for key, value in zip(technicians, row[1:]):
                if value:
                    technicians[key] = find_info(value)
            log.debug(f"Found technicians in google sheets: {technicians}")
            return technicians

    log.warning(f"Didn't find any technicians in google sheets for date: {date}")
    return technicians
