from flask import Blueprint, request, jsonify
from supabase_client import supabase
from ..auth import verify_token
import uuid, mimetypes

bp = Blueprint('courses', __name__, url_prefix='/courses')

# returns departments
@bp.route('/', methods=['GET'])
def index():
    # frontend passes this in their headers
    # "Authorization": "Bearer " + access_token

    # Get token from Authorization header
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    # for debugging purposes, even if no/invalid token is passed, still return data
    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")
        # return json of no token or invalid token

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
        return jsonify({"response": "500", "error": str(exception)}), 500


# endpoint to return all courses for a department
@bp.route('/<string:department>', methods=['GET'])
def getCourses(department):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    # for debugging purposes, even if no/invalid token is passed, still return data
    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

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

            # course_name is made for frontend, course_name_backend
            # course_name_backend is how course name is stored in database as is
            # frontend will pass in course_name_backend to any future calls when referring to a course
            newCourse = {
                "course_code": course_code,
                "course_name": course_name,
                "course_name_backend": course["course_name"],
                "course_id": course["course_id"]
            }

            modifiedCourses.append(newCourse)

        return jsonify(modifiedCourses), 200

    except Exception as exception:
        return jsonify({"response": "500", "error": str(exception)}), 500

# post a public file in a specific course
@bp.post('/<string:course_name_backend>/files')
def uploadFile(course_name_backend):
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
    title = request.form.get("title")

    # course_name will be course_name_backend
    # course_name = request.form.get("course_name")
    user_id = request.form.get("user_id")

    if user_id:
        user_id = user_id.strip('"')  # remove extra double quotes

    # file path will be saves as UUID_filename.extension
    file_path = f"{note_id}_{file.filename}"
    bucket_path = f"{note_id}_{file.filename}"

    new_note = {
        "note_id": note_id,
        "is_public": True,
        "title": title,
        "file_path": file_path, # actual hosted path
        "bucket_path": bucket_path, # path in bucket
        "course_name": course_name_backend,
        "user_id": user_id,
        "room_id": None
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

# this will fetch all public files in a course like Calc 1 and any files that were uploaded as public inside rooms
@bp.get('/<string:course_name_backend>/files')
def getCourseNotes(course_name_backend):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

    try:
        get_response = (
            supabase
            .table("notes")
            .select("*")
            .eq("course_name", course_name_backend)
            .eq("is_public", True)
            .execute()
        )

        if get_response.data:
            return jsonify(get_response.data)
        else:
            return jsonify([])

    except Exception as e:
        return jsonify({"error": str(e)})

# delete a file
@bp.delete('/<string:file_id>')
def deleteNote(file_id):
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if verify_token(token):
        print("success, will allow for endpoint")
    else:
        print("do not return data")

    try:
        table_response = supabase.table("notes").select("*").eq("note_id", file_id).execute()
        if table_response.data:
            bucket_path = table_response.data[0]["bucket_path"]
            # for some reason to delete has to be an array
            del_response = supabase.storage.from_("notes").remove([bucket_path])
        
        try:
            delete_response = supabase.table("notes").delete().eq("note_id", file_id).execute()

            return jsonify({"response": "successfully deleted note"}), 200
            
        except Exception as exception:
            return jsonify({"error": str(exception)}), 500

    
    except Exception as e:
        return jsonify({"error": str(e)}), 500