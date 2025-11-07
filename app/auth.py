# file that will handle routes for auth like login and logout
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')

# supabase already handles auth

