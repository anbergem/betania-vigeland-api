import datetime
import json
import logging
import os

import flask
import requests.auth

from .blueprint import bp
from ...src.google_sheets.service import get_technicians_for_date
from ...src.planning_center.team import get_people

log = logging.getLogger("bva")


def create_plan_person(service_type_id, plan_id, team_id: int, team_position_name: str, person_id: int, auth):
    url = f"https://api.planningcenteronline.com/services/v2/service_types/{service_type_id}/plans/{plan_id}/team_members"
    data = {
        "data": {
            "attributes": {
                "team_id": team_id,
                "team_position_name": team_position_name,
                "person_id": person_id,
                "status": "Confirmed"
            }
        }
    }
    response = requests.post(url, json=data, auth=auth)
    if response.status_code != 201:
        log.warning(f"Could not create plan person: {response.reason}")
        log.debug(json.dumps(response.json()))
        return False

    log.debug(f"Successfully created plan person for {person_id}")
    return True


def set_technicians_for_date(service_type_id: int, plan_id: int, date: datetime.date, auth: requests.auth.HTTPBasicAuth):
    technician_names = get_technicians_for_date(date)
    # Todo: Move somewhere
    technicians_team_id = 1372212
    result = {}
    for position, name in technician_names.items():
        if name is None:
            continue
        technicians = get_people(auth, where=("search_name", name))
        if len(technicians) != 1:
            log.warning(f"Expected to find 1 technician, found {len(technicians)}")
            if len(technicians) > 1:
                log.warning(f"\t{','.join([technician.name for technician in technicians])}")
            return

        success = create_plan_person(service_type_id, plan_id, technicians_team_id, position, technicians[0].id, auth)
        if success:
            log.info(f"Successfully set {name} to {position}")
            result[position] = name

    return result


@bp.route("/plan-created", methods=["POST"])
def plan_created():
    if not flask.request.is_json:
        log.warning("Plan created post request not in json format")
        return json.dumps({"success": False})

    data = flask.request.json["data"][0]["attributes"]
    payload = json.loads(data["payload"])

    service_type_id = payload["data"]["relationships"]["service_type"]["data"]["id"]

    meeting_service_id = 368342  # M??te Betania Vigeland

    if int(service_type_id) == meeting_service_id:
        plan_id = int(payload["data"]["id"])
        try:
            date = datetime.datetime.strptime(payload["data"]["attributes"]["dates"], "%d %B %Y").date()
        except ValueError:
            log.debug("Returning due to no valid dates")
            return json.dumps({
                "success": False,
                "message": "No valid dates"
            })
        auth = requests.auth.HTTPBasicAuth(os.getenv("USERNAME"), os.getenv("PASSWORD"))
        positions = set_technicians_for_date(meeting_service_id, plan_id, date, auth)
        return json.dumps({
            "success": True,
            "message": positions
        })

    return json.dumps({
        "success": False,
        "message": "Non-relevant service id"
    })
