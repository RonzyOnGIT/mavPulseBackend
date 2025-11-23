from flask import Blueprint, request, jsonify
from supabase_client import supabase
from ..auth import verify_token
from .user import getUserName
import uuid
import mimetypes


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

# TODO: cleanup timestamp to make frontend's job easier
# returns chat for a room
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


# send a message
# @bp.route('/<string:room_id>', methods=["POST"])
# def sendMessage(room_id):

#     auth_header = request.headers.get("Authorization", "")
#     token = auth_header.replace("Bearer ", "")

#     if verify_token(token):
#         print("success, will allow for endpoint")
#     else:
#         print("do not return data")
    
#     data = request.get_json()

#   update the room's size here as well


#     try:
#         new_message_query = supabase.table("messages").insert().execute()
#     except Exception as exception:

# work on creating a room
# @bp.route('/rooms', methods=['POST'])
# def createRoom():
#     auth_header = request.headers.get("Authorization", "")
#     token = auth_header.replace("Bearer ", "")

#     if verify_token(token):
#         print("success, will allow for endpoint")
#     else:
#         print("do not return data")

#     if not request.is_json:
#         return jsonify({"response": "400", "error": "Request must be JSON"}), 400

#     data = request.get_json()

#     course_id = data.get("course_id")
#     creator_id = data.get("creator_id")
#     room_name = data.get("name")

#     new_room = {
#         "course_id": course_id,
#         "creator_id": creator_id,
#         "room_name": room_name
#     }

#     try:
#         post_response = supabase.table("rooms").insert(new_room).execute()

#         if post_response.error:
#             return jsonify({"error": post_response.error})
    
#         return jsonify(post_response.data)
        
#     except Exception as exception:
#         return jsonify({"error": str(exception)})


# upload a file inside a room
@bp.post('/<string:room_id>/files')
def uploadFile(room_id):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

    file = request.files.get("file")

    if file is None:
        return {"error": "No file uploaded"}, 400

    BASE_URL = 'https://kknornzfiytxjuzjpdom.supabase.co/storage/v1/object/public/notes'
    note_id = str(uuid.uuid4())
    is_public = request.form.get("is_public") == "true"
    title = request.form.get("title")

    # course_name will be course_name_backend
    course_name = request.form.get("course_name")
    user_id = request.form.get("user_id")

    if user_id:
        user_id = user_id.strip('"')  # remove extra double quotes

    # file path will be saves as UUID_filename.extension
    file_path = f"{note_id}_{file.filename}"
    bucket_path = f"{note_id}_{file.filename}"

    new_note = {
        "note_id": note_id,
        "is_public": is_public,
        "title": title,
        "file_path": file_path, # actual hosted path
        "bucket_path": bucket_path, # path in bucket
        "course_name": course_name,
        "user_id": user_id,
        "room_id": room_id
    }

    file_bytes = file.read()

    # this is to be able to tell supabase what type of file it is
    content_type, _ = mimetypes.guess_type(file.filename)

    upload_request = supabase.storage.from_("notes").upload(file_path, file_bytes, {"content-type": content_type})

    try:
        # store in the notes table the path to the file in the bucket
        new_note["file_path"] = f"{BASE_URL}/{file_path}"
        notes_request = supabase.table("notes").insert(new_note).execute()
    
        if notes_request.data:
            return jsonify(notes_request.data), 201      

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# fetch all notes from a room
@bp.get('/<string:room_id>/files')
def getFilesFromRoom(room_id):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")
    
    try: 
        files_response = supabase.table("notes").select("*").eq("room_id",).execute()

        if files_response.data:
            return jsonify(files_response.data)
        else:
            return jsonify([])
            
    except Exception as e:
        return jsonify({"error": str(e)})



'''
    user A has privat and public key. 
    They want to create a new room so they generate some room key, ROOM_KEY_AES, which uses A's public key to encrypt
    And a new room of id 123 is created as well as new row in room_members with key column being encrypted room key for A
    This encrypted key is then stored in room_members table as ROOM_KEY_AES_A or something

    
    If user A wants to send a message, it encrypts their message using public ROOM_KEY_AES
    and makes entry in messages table

    User B comes along and want to join room, in order to be able to join room, B needs to know the rooms public symmetric key
    The problem is that only user A knows it not the server or database since its encrypted

    So user B would send a request to user A passing in user B's public key
    So if user A approves user B request to join then it would take the original room key and encrypt it using B's public key
    Then a new entry in the table is made in the room_members table with ROOM_key_AES_B
    Now user B would go to table to get the ROOM_KEY_AES_B and using B's private key decrypt it to get original room key
    Now user B can user this key to encrypt messages to room and stuff like that

'''




    