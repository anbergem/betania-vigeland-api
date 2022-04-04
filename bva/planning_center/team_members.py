import collections
import json
import logging

import flask
import requests.auth

from .blueprint import bp


@bp.route("/get-confirmed-team-members", methods=["GET"])
def get_confirmed_team_members():
    url = "https://api.planningcenteronline.com/services/v2/service_types/368342/plans/58206001"

    auth = flask.request.authorization

    if auth is None:
        logging.info("Unauthorized access requested")
        return "Bad request: Authorization required", 400

    response = requests.get(url + "/team_members?per_page=100&include=team", auth=requests.auth.HTTPBasicAuth(auth.username, auth.password))
    data = response.json()
    team_members = collections.defaultdict(lambda: collections.defaultdict(set))
    team_map = {}
    person_map = {}
    for inclusion in data["included"]:
        if inclusion["type"] == "Team":
            team_map[inclusion["id"]] = inclusion["attributes"]["name"]
        elif inclusion["type"] == "Person":
            person_map[inclusion["id"]] = inclusion["attributes"]["name"]

    for person in data["data"]:
        team = person["relationships"]["team"]["data"]["id"]
        if team not in team_map:
            raise RuntimeError(f"Team not in included teams: {team}")
        team_members[team_map[team]][person["attributes"]["team_position_name"]].add(person["attributes"]["name"])

    def serialize_sets(obj):
        if isinstance(obj, set):
            return list(obj)
        return obj

    return json.dumps(team_members, default=serialize_sets)
