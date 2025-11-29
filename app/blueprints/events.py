from flask import Blueprint, request, jsonify
from supabase_client import supabase
from ..auth import verify_token
from .user import getUserName

bp = Blueprint('events', __name__, url_prefix='/events')

# want to have just an endpoint to return all events
@bp.route('/', methods=['GET'])
def index():

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")
    
    # how many events to return
    limit = request.args.get("limit", type=int)

    # offset to avoid retrieving old data
    offset = request.args.get("offset", type=int)
 
    try:
        events_query = supabase.table("events").select("*")

        if limit is not None and offset is not None:
            events_query = events_query.range(offset, offset + limit - 1)
        elif limit: 
            events_query = events_query.limit(limit)
        
        events_response = events_query.execute()

        if events_response.data:
            return jsonify(events_response.data)
        else:
            return jsonify([])

    except Exception as exception:
        return jsonify({"response": "500", "error": str(exception)}), 500

