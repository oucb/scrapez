from flask import session
from flask_socketio import emit, join_room, leave_room
from apps.ui.extensions import socketio

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room', 'default')
    name = session.get('name', 'unknown')
    join_room(room)
    print("Client '%s' joined the room: %s" % (name, room))
    emit('status', {'msg': name + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room', 'default')
    name = session.get('name', 'unknown')
    print("Received '%s' from '%s' in room '%s'" % (message, name, room))
    emit('message', {'msg': name + ': ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room', 'default')
    name = session.get('name', 'unknown')
    leave_room(room)
    print("Client '%s' left room '%s'" % (name, room))
    emit('status', {'msg': name + ' has left the room.'}, room=room)
