import datetime
import typing

from .sheets import read_spreadsheet


def get_technicians_for_date(date: datetime.date) -> typing.Optional[typing.Dict[str, str]]:
    spreadshet_id = "1nNVrzcVQFULWVans5zt3N0_tqsl6U9U1hzGV_mhseJ4"
    range = "A2:C"

    rows = read_spreadsheet(spreadshet_id, range)
    # Todo: Put model somewhere else
    technicians = {"PC": None, "Lyd": None}

    for row in rows:
        if not row:
            continue
        value_date = datetime.datetime.strptime(row[0], "%d. %B %Y").date()
        if value_date == date:
            for key, value in zip(technicians, row[1:]):
                if value:
                    technicians[key] = value
            return technicians
    return
