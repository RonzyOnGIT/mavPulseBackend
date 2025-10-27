# file that will handle routes for auth like login and logout
from flask import Blueprint
from flask_jwt_extended import create_access_token


bp = Blueprint('auth', __name__, url_prefix='/auth')
