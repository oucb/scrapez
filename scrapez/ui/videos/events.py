# from flask import session
# from flask_socketio import emit, join_room, leave_room
# from ..extensions import socketio

# @socketio.on('search_done', namespace='/video')
# def joined(message):
#     """Sent by clients when they enter a room.
#     A status message is broadcast to all people in the room."""
#     print("Finished searching")
#     emit('clear')
