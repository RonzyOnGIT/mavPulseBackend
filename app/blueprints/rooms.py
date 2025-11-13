from flask import Blueprint, request, jsonify
from supabase_client import supabase
from ..auth import verify_token
from .user import getUserName


bp = Blueprint('rooms', __name__, url_prefix='/rooms')

# fetches all rooms for specific course
@bp.route('/<string:course_name_backend>', methods=['GET'])
def getRooms(course_name_backend):

    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

    try:
        course_result = supabase.table("courses").select("course_id").eq("course_name", course_name_backend).execute()

        course_id = course_result.data[0]['course_id']
        rooms_result = supabase.table("rooms").select("*").eq("course_id", course_id).execute()

        rooms = []

        for room in rooms_result.data:
            owner_name = getUserName(room["creator_id"])
            room_name = room["room_name"]

            new_room = {
                "owner": owner_name,
                "room_name": room_name,
                "members": room["size"]
            }

            rooms.append(new_room)
        
        return jsonify(rooms), 200

    except Exception as exception:
        return jsonify({"response": "500", "error": str(exception)}), 500
    
