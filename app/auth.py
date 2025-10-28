# file that will handle routes for auth like login and logout
from flask import Blueprint
from flask_jwt_extended import create_access_token

from app.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


# need to work on actual auth
# @bp.route('/register', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':

