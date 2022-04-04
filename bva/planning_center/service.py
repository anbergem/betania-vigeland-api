import json
import logging

import flask

from .blueprint import bp


@bp.route("/service-created", methods=["POST"])
def service_created():
    logging.warning("Service ")
    if flask.request.is_json:
        logging.warning("Json data")
        logging.warning(json.dumps(flask.request.json))
    else:
        form = flask.request.form
        for key, value in form.items():
            logging.warning("Forms data")
            logging.warning(f"{key}: {value}")

    return json.dumps({})
