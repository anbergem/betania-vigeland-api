import json
import logging

import flask

from .blueprint import bp


@bp.route("/service-created", methods=["POST"])
def service_created():
    logging.info("Service ")
    if flask.request.is_json:
        logging.info("Json data")
        logging.info(json.dumps(flask.request.json))
    else:
        form = flask.request.form
        for key, value in form.items():
            logging.info("Forms data")
            logging.info(f"{key}: {value}")

    return json.dumps({})
