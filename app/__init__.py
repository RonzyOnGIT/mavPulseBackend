# application factory
from flask import Flask
from . import auth
from . import db
import os

# application factory function
def create_app(test_config = None) -> Flask:
    # create and config app

    # instance_relative_config=True tells app that config files are relative to 'instance' folder-
    # since the instance folder is not in the same package as app
    app = Flask(__name__, instance_relative_config=True)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, "app.db")
    )

    db.init_app(app)  # Connect SQLAlchemy to the Flask app

    # register auth blueprint to app
    app.register_blueprint(auth.bp)

    # To Do: initialize database with app, and check if empty or not
    return app


    

