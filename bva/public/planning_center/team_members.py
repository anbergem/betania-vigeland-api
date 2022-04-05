import json
import logging

import flask

from .blueprint import bp
from ...src.planning_center.team import get_team_members


@bp.route("/get-confirmed-team-members", methods=["GET"])
def get_confirmed_team_members():
    auth = flask.request.authorization

    if auth is None:
        logging.info("Unauthorized access requested")
        return "Bad request: Authorization required", 400

    team_members = get_team_members(58206001, auth)

    def serialize_sets(obj):
        if isinstance(obj, set):
            return list(obj)
        return obj

    return json.dumps(team_members, default=serialize_sets)
