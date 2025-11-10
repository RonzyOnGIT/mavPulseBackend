# file that will handle routes for auth like login and logout
from flask import Blueprint, request, jsonify
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
    
    if emailSplit[1] != "mavs.uta.edu":
        return jsonify({"error": "Invalid UTA email"}), 400
    
    try:
        response = supabase.auth.sign_up({
            "username": username,
            "email": email,
            "password": password
        })

        # rate limit of 2 new users per hour :(
        # if response.user:
        #     return jsonify({"message": "user succesfully created"}), 201
        # frontend will then make a call in the /login endpoint to retrive token if user confirms

        if response.user:

            access_token = response.session.access_token
            expires_in = response.session.expires_in # 1 hour in seconds
            expires_at = response.session.expires_at # the exact time in seconds when it expires
            refresh_token = response.session.refresh_token
            
            user_id = response.user.id
            
            try:
                db_response = supabase.table("users").insert({
                    "id": user_id,
                    "username": username,
                    "email": email,
                }).execute()


                response_data = {
                    "message": "user successfully created!",
                    "access_token": access_token,
                    "expires_at": expires_at,
                    "expires_in": expires_in,
                    "refresh_token": refresh_token,
                }

                return jsonify(response_data), 201
            
            except Exception as exception:
                return jsonify({"response": "500", "error": str(exception)}), 500

        # if response.user:
        #     return jsonify({"response": "201", "message": "please check your email to confirm your account"}), 201
    
    except Exception as e:
        return jsonify({"response": "500", "error": str(e)}), 500
    


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
    
# need a third endpoint for refreshting access_tokens using refresh_token