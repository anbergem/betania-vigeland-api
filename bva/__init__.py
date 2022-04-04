import logging

from flask import Flask

from .planning_center import bp as planning_center_bp


def create_app():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(planning_center_bp)

    return app
