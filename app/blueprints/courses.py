from flask import Blueprint, request, jsonify
from supabase_client import supabase

bp = Blueprint('courses', __name__, url_prefix='/courses')


# returns departments
@bp.route('/', methods=['GET'])
def index():

    # how many departments to return
    limit = request.args.get('limit', type=int)

    # offset to avoid retrieving old data
    offset = request.args.get('offset', type=int)

    try:

        departmentsQuery = supabase.table("departments").select("*")

        if limit is not None and offset is not None:
            departmentsQuery = departmentsQuery.range(offset, offset + limit - 1)
        elif limit: 
            departmentsQuery = departmentsQuery.limit(limit)
        
        # no need to do try catch since it doesnt raise an exception
        departmentResponse = departmentsQuery.execute()

        return jsonify(departmentResponse.data)

    except Exception as exception:
        return jsonify({"response": "500", "error": exception}), 500
    

