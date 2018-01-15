from flask_socketio import SocketIO
from flask_jsglue import JSGlue
import eventlet
eventlet.monkey_patch(socket=True)

socketio = SocketIO()
jsglue = JSGlue()

EXTENSIONS = [
    # (socketio, {'message_queue': 'redis://'}),
    (socketio, {'message_queue': 'redis://localhost', 'async_mode': 'eventlet'}),
    # socketio,
    jsglue
]
