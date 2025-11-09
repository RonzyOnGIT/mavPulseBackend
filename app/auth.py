# file that will handle routes for auth like login and logout
from flask import Blueprint, request, jsonify
from app.db import get_db
from supabase_client import supabase


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"response": "400", "error": "Request must be JSON"}), 400

    # get json from post request
    data = request.get_json()

    # extract fields from json
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    

    # for now assume frontend does not check for email type
    if "@" not in email:
        return jsonify({"error": "Missing @"}), 400
    
    emailSplit = email.split("@")
    
    if emailSplit[1] != "@mavs.uta.edu":
        return jsonify({"error": "Invalid UTA email"}), 400
    
    try:
        response = supabase.auth.sign_up({
            "username": username,
            "email": email,
            "password": password
        })

        # successfully created user, user now needs to confirm using their email
        # frontend will then make a call in the /login endpoint to retrive token if user confirms
        if response.user:
            return jsonify({"response": "201", "message": "please check your email to confirm your account"}), 201
    
    except Exception as e:
        return jsonify({"response": "500", "error": str(e)})
    


@bp.route('/login', methods=['GET'])
def login():
    
    if not request.is_json:
        return jsonify({"error": "Response must be JSON"}), 400

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    try:
        response = supabase.auth.sin_in_with_password(email=email, password=password)
        if response.session:
            return jsonify({"response": "200", "acessToken": response.session.access_token})
    except Exception as e:
        return jsonify({"response": "500", "error": str(e)})

