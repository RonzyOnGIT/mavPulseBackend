from flask import Blueprint, request, jsonify
from supabase_client import supabase
from ..auth import verify_token



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