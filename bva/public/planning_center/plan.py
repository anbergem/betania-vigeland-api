import json
import logging

import flask

from .blueprint import bp


@bp.route("/plan-created", methods=["POST"])
def plan_created():
    if flask.request.is_json:
        logging.warning("Plan created post request not in json format")
        return json.dumps({"success": False})

    data = flask.request.json
    payload = json.loads(data["payload"])

    plan_id = payload["data"]["id"]



    return json.dumps({"success": True})
