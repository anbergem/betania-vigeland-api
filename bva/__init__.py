from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from .planning_center import bp as planning_center_bp
    app.register_blueprint(planning_center_bp)

    return app
