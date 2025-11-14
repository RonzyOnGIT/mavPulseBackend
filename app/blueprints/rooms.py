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
                "members": room["size"],
                "room_id": room["id"]
            }

            rooms.append(new_room)
        
        return jsonify(rooms), 200

    except Exception as exception:
        return jsonify({"response": "500", "error": str(exception)}), 500

# need to get room id because room name can be duplicates
# TODO: cleanup timestamp to make frontend's job easier
@bp.route('/chat/<string:room_id>', methods=["GET"])
def getChat(room_id):

    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

    # Get limit from query params, default to 50
    limit = request.args.get("limit", type=int)
    # offset = request.args.get("offset", type=int)

    # queries messages table to get all entries with specified room id
    # returns the messages from oldest to newest
    messages_query = supabase.table("messages").select("*").eq("room_id", room_id).order("created_at", desc=True).limit(limit).execute()

    messages = []

    for i in range(len(messages_query.data)):
        retrieved_message = messages_query.data[i]

        message_id = retrieved_message["message_id"]
        sender_id = retrieved_message["sender_id"]
        timestamp = retrieved_message["created_at"]
        user = retrieved_message["sender_name"]
        content = retrieved_message["content"]

        new_message = {
            "message_id": message_id,
            "user_id": sender_id,
            "timestamp": timestamp,
            "username": user,
            "content": content
        }

        messages.append(new_message)

    return jsonify(messages)

# TODO: endpoint for creating entry in messages table (sending message)


    