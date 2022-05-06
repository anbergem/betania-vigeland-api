from flask import Flask

from .public.planning_center import bp as planning_center_bp
from .utils import *


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(planning_center_bp)

    return app
