# application factory
from flask import Flask


# application factory function
def create_app(test_config = None) -> Flask:
    # create and config app
    app = Flask(__name__)

    # To Do: initialize database with app, and check if empty or not

    return app


    

