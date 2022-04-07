import datetime
import json
import logging

import flask
import requests.auth

from config import USERNAME, PASSWORD
from .blueprint import bp
from ...src.planning_center.team import get_people


def get_technician_name_for_date(date: datetime.date) -> str:
    return "Andreas Bergem"


def create_plan_person(team_id: int, team_position_name: str, person_id: int, auth):
    url = f"https://api.planningcenteronline.com/services/v2/service_types/368342/plans/58318974/schedule_team_members"
    data = {"data": {"attributes": {"team_id": team_id, "team_position_name": team_position_name, "people_ids": [person_id]}}}
    response = requests.post(url, json=data, auth=auth)
    if response.status_code != 201:
        logging.warning(f"Could not create plan person: {response.reason}")
        logging.debug(json.dumps(response.json()))


def set_technician_for_date(auth: requests.auth.HTTPBasicAuth, date: datetime.date):
    technician_name = get_technician_name_for_date(date)
    technicians = get_people(auth, where=("search_name", technician_name))  # 71247615
    if len(technicians) != 1:
        logging.warning(f"Expected to find 1 technician, found {len(technicians)}")
        if len(technicians) > 1:
            logging.warning(f"\t{','.join([technician.name for technician in technicians])}")
        return
    team_id = 1372212
    create_plan_person(team_id, "PC", technicians[0].id, auth)


@bp.route("/plan-created", methods=["POST"])
def plan_created():
    if flask.request.is_json:
        logging.warning("Plan created post request not in json format")
        return json.dumps({"success": False})

    data = flask.request.json
    payload = json.loads(data["payload"])

    service_type_id = payload["data"]["relationships"]["service_type"]["data"]["id"]

    # Møte Betania Vigeland
    if service_type_id == 368342:
        date = datetime.datetime.strptime(payload["data"]["attributes"]["dates"], "%d %B %Y").date()
        auth = requests.auth.HTTPBasicAuth(USERNAME, PASSWORD)
        set_technician_for_date(auth, date)

    return json.dumps({"success": True})
