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


# endpoint to return all courses for a department
@bp.route('/<string:department>', methods=['GET'])
def getCourses(department):

    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)

    try:
        coursesQuery = supabase.table("courses").select("*").ilike("department", department + " ")

        if limit is not None and offset is not None:
            coursesQuery = coursesQuery.range(offset, offset + limit - 1)
        elif limit:
            coursesQuery = coursesQuery.limit(limit)

        coursesResponse = coursesQuery.execute()

        modifiedCourses = []

        # change format to array of objects: {"course_code": "ACCT 101", "course_name": "Introduction to Accounting"}
        for course in coursesResponse.data:
            course_code_arr = course["course_name"].split(" ")
            course_code = course_code_arr[0] + " " + course_code_arr[1]
            course_name_arr = course_code_arr[3:]
            course_name = " ".join(course_name_arr)

            newCourse = {"course_code": course_code, "course_name": course_name}
            modifiedCourses.append(newCourse)

        return jsonify(modifiedCourses), 200

    except Exception as exception:
        return jsonify({"response": "500", "error": str(exception)}), 500
    

