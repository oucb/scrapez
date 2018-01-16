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
    name = session.get('name') or message.get('name', 'unknown')
    msg = message['msg']
    full_msg = name + ': ' + msg
    print("Chat message --> %s (room '%s')" % (full_msg, room))
    emit('message', {'msg': full_msg}, room=room)

@socketio.on('change_name', namespace='/chat')
def text(message):
    old_name = session.get('name', 'unknown')
    new_name = message.get('name', 'unknown')
    if not new_name == old_name:
        print("'%s' changed name to '%s'" % (old_name, new_name))
        emit('name_changed', {old_name: old_name, new_name: new_name})

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room', 'default')
    name = session.get('name', 'unknown')
    leave_room(room)
    print("Client '%s' left room '%s'" % (name, room))
    emit('status', {'msg': name + ' has left the room.'}, room=room)
