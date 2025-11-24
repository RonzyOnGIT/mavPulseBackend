from flask import Blueprint, request, jsonify
from supabase_client import supabase
from ..auth import verify_token

bp = Blueprint('user', __name__, url_prefix='/user')

def getUserName(user_id):
    
    try:

        userQuery = supabase.table('users').select('*').eq('user_id', user_id).execute()

        if userQuery.data:
            return userQuery.data[0]['username']
        else:
            return None
        
    except Exception as exception:
        print(str(exception))
        return None


@bp.get('/notes/<string:user_id>')
def getUserNotes(user_id):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")
    
    try:
        notes_request = supabase.table("notes").select("*").eq("user_id", user_id).execute()

        if notes_request.data:
            return jsonify(notes_request.data)
        else:
            return jsonify([])
    except Exception as exception:
        return jsonify({"error": str(exception)})


@bp.post('/favorites')
def favoriteNote():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")
    
    data = request.get_json()

    note_id = data.get("note_id")
    user_id = data.get("user_id")

    new_favorite = {
        "note_id": note_id,
        "user_id": user_id
    }
    
    try:
        post_request = supabase.table("favorite_notes").insert(new_favorite).execute()
    
        if post_request.data:
            return jsonify(post_request.data[0])
        else:
            return jsonify([])
    except Exception as exception:
        return jsonify({"error": str(exception)})


# @bp.get('/favorites/<string:user_id>')
# def getFavorites(user_id):
#     auth_header = request.headers.get("Authorization", "")
#     token = auth_header.replace("Bearer ", "")

#     if verify_token(token):
#         print("success, will allow for endpoint")
#     else:
#         print("do not return data")
    
#     try:
#         notes_request = supabase.table("favorite_notes").select("*").eq("user_id", user_id).execute()

#         # notes_request = (
#         #     supabase
#         #         .table("favorite_notes")
#         #         .select("note_id, notes(*)")
#         #         .eq("user_id", user_id)
#         #         .execute()
#         # )


#         if notes_request.data:
#             return jsonify(notes_request.data)
#         else:
#             return jsonify([])
#     except Exception as exception:
#         return jsonify({"error": str(exception)})
