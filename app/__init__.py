# application factory
from flask import Flask
from . import auth


# application factory function
def create_app(test_config = None) -> Flask:
    # create and config app
    app = Flask(__name__)

    # register auth blueprint to app
    app.register_blueprint(auth.bp)

    # To Do: initialize database with app, and check if empty or not

    return app


    

