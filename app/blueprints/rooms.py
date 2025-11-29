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
@bp.route('/chat/<string:room_id>', methods=["POST"])
def sendMessage(room_id):

    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")
    
    
    data = request.get_json()

    sender_id = data.get("sender_id")
    content = data.get("content")
    sender_name = data.get("sender_name")

    new_message = {
        "sender_id": sender_id,
        "content": content,
        "sender_name": sender_name,
        "room_id": room_id
    }

    try:
        check_message_count = supabase.table("rooms").select("*").eq("id", room_id).execute()

        check_user_message_count = supabase.table("users").select("*").eq("user_id", sender_id).execute()

        if check_message_count.data and check_user_message_count.data:
            # check to make sure havent reached max message count of room and
            # check to make sure user hasnt exceeded max messages
            room_message_count = check_message_count.data[0]["message_count"]
            user_message_count = check_user_message_count.data[0]["total_messages"]
            if room_message_count >= 300 or user_message_count >= 500:

                return jsonify({"error": "max message count reached"}), 400

            try:
                new_message_response = supabase.table("messages").insert(new_message).execute()

                if new_message_response.data:
                    supabase.table("rooms").update({"message_count": room_message_count + 1}).eq("id", room_id).execute()
                    supabase.table("users").update({"total_messages": user_message_count + 1}).eq("user_id", sender_id).execute()
                    return jsonify(new_message_response.data[0])

            except Exception as err:
                return jsonify({"error": str(err)})
        else:
            return jsonify({"error": "room not found"})

    except Exception as exception:
        return jsonify({"error": str(exception)})
    
@bp.delete('/chat/<string:message_id>')
def deleteMessage(message_id: str):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")    

    try:

        del_response = supabase.table("messages").delete().eq("message_id", message_id).execute()

        if del_response.data:
            return jsonify(del_response.data[0])
    except Exception as err:
        return jsonify({"error": str(err)}), 500


# create room
@bp.route('/new_room', methods=['POST'])
def createRoom():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

    if not request.is_json:
        return jsonify({"response": "400", "error": "Request must be JSON"}), 400

    data = request.get_json()

    course_id = data.get("course_id")
    creator_id = data.get("creator_id")
    room_name = data.get("name")

    # role can be 'owner' or 'member'
    role = data.get("role")
    encrypted_key = data.get("encrypted_room_key")
    room_id = str(uuid.uuid4())

    new_room = {
        "course_id": course_id,
        "creator_id": creator_id,
        "room_name": room_name,
        "size": 1,
        "id": room_id
    }

    new_room_member = {
        "room_id": room_id,
        "user_id": creator_id,
        "role": role,
        "encrypted_room_key": encrypted_key
    }

    try:
        # first make new entry in rooms table
        room_post_response = supabase.table("rooms").insert(new_room).execute()

        if room_post_response.data:
            try:
                # now make new entry in room_members table
                member_post_response = supabase.table("room_members").insert(new_room_member).execute()

                if member_post_response.data:

                    success_response = {
                        "room": room_post_response.data[0],
                        "member": member_post_response.data[0]
                    }

                    return jsonify(success_response)

                else:
                    return jsonify([])

            except Exception as e:
                return jsonify({"error": str(e)})

        else:
            return jsonify([])
            
    except Exception as exception:
        return jsonify({"error": str(exception)})


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


# user request to join room, new entry is made in table called requests
@bp.post('/<string:room_id>')
def joinRoomRequest(room_id):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

    data = request.get_json()

    # requester passes his public key
    requester_key = data.get("user_key")
    requester_name = data.get("username")
    requester_id = data.get("user_id")

    new_request = {
        "requester_key": requester_key,
        "requester_name": requester_name,
        "requester_id": requester_id,
        "room_id": room_id       
    }

    try: 
        # first need to check if user is already a member, and or if they are pending request
        try:
            # first check to see if there is a request pending
            pending_res = supabase.table("requests").select("*").eq("room_id", room_id).eq("requester_id", requester_id).execute()

            if pending_res.data:
                return jsonify({"error": "user already has pending request"})
            
            # now check to see if they are already member, to return the key to be able to decrypt
            already_member_res = supabase.table("room_members").select("*").eq("user_id", requester_id).eq("room_id", room_id).execute()

            # user was granted permission, return stuff, need to delete request entry now
            if already_member_res.data:
                del_response = supabase.table("requests").delete().eq("room_id", room_id).eq("requester_id", requester_id).execute()

                if del_response.data:
                    return jsonify(already_member_res.data[0])
        except Exception as err:
            return jsonify({"error": str(err)})

        request_reponse = supabase.table("requests").insert(new_request).execute()

        if request_reponse.data:
            return jsonify(request_reponse.data)
        else:
            return jsonify([])
            
    except Exception as e:
        return jsonify({"error": str(e)})    


# returns pending request to join room
@bp.get('/<string:room_id>/<string:user_id>')
def checkPendingRequests(room_id, user_id):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

    # first check to see if this person is the owner of the room
    try: 
        room_reponse = supabase.table("rooms").select("*").eq("id", room_id).execute()
    
        if room_reponse.data:
            # check to see if user is owner
            if room_reponse.data[0]["creator_id"] == user_id:
                # they are the owner, good to check for requests
                try:
                    request_response = supabase.table("requests").select("*").eq("room_id", room_id)
                    if request_response.data:
                        return jsonify(request_response.data)
                    else:
                        return jsonify([])
                except Exception as err:
                    return jsonify({"error": str(err)})      
            else:
                return jsonify({"error": "user is not owner"})
            
    except Exception as e:
        return jsonify({"error": str(e)})   


@bp.post('/<string:room_id>/<string:request_id>') 
def acceptRequest(room_id, request_id):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

    data = request.get_json()

    user_id = data.get("user_id")
    encrypted_key = data.get("encrypted_key")

    try: 
        room_reponse = supabase.table("rooms").select("*").eq("id", room_id).execute()
    
        if room_reponse.data:
            # check to see if user is owner
            if room_reponse.data[0]["creator_id"] == user_id:
                # they are the owner, make new entry in room_members to allow new member
                try:
                    # look up the request to get the requester id to make new entry in room_members
                    requests_response = supabase.table("requests").select("*").eq("request_id", request_id).execute()
                    if requests_response.data:
                        new_member = {
                            "room_id": room_id,
                            "user_id": requests_response.data[0]["requester_id"],
                            "role": "member",
                            "encrypted_room_key": encrypted_key
                        }

                        member_response = supabase.table("room_members").insert(new_member).execute()
                        if member_response.data:
                            return jsonify(member_response.data)

                except Exception as e:
                    return jsonify({"error": str(e)})
                
            else:
                return jsonify({"error": "user is not owner"})
            
    except Exception as e:
        return jsonify({"error": str(e)}) 

    
    


    


'''
    user A has privat and public key. 
    They want to create a new room so they generate some room key, ROOM_KEY, which uses A's public key to encrypt
    And a new room of id 123 is created as well as new row in room_members with key column being encrypted room key for A
    This encrypted key is then stored in room_members table as ROOM_KEY_A or something

    
    If user A wants to send a message, it encrypts their message using public ROOM_KEY
    and makes entry in messages table

    User B comes along and want to join room, in order to be able to join room, B needs to know the rooms public symmetric key
    The problem is that only user A knows it not the server or database since its encrypted

    So user B would send a request to user A passing in user B's public key
    So if user A approves user B request to join then it would take the original room key and encrypt it using B's public key
    Then a new entry in the table is made in the room_members table with ROOM_key_AES_B
    Now user B would go to table to get the ROOM_KEY_AES_B and using B's private key decrypt it to get original room key
    Now user B can user this key to encrypt messages to room and stuff like that

'''




    