from flask_socketio import SocketIO
from flask import request


socketio = SocketIO(cors_allowed_origins="*")

# Keep track of connected users
connected_users = {}


# https://mavpulsebackend.onrender.com:5000/socket.io/?user_id=$userId
# debugging: http://127.0.0.1:5000/socket.io/?user_id=$userId
@socketio.on('connect')
def handle_connect(auth):
    user_id = auth.get('user_id') if auth else None    
    if user_id:
        connected_users[user_id] = request.sid
        print(f"User {user_id} connected with SID {request.sid}")


@socketio.on('disconnect')
def handle_disconnect():
    for uid, sid in list(connected_users.items()):
        if sid == request.sid:
            connected_users.pop(uid)
            print(f"User {uid} disconnected")
            break
