from flask_socketio import SocketIO
from flask_jsglue import JSGlue
from flask_caching import Cache
import eventlet
eventlet.monkey_patch(socket=True)

socketio = SocketIO()
jsglue = JSGlue()
cache = Cache()

EXTENSIONS = [
    (cache, {'config': {'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost'}}),
    (socketio, {'message_queue': 'redis://localhost', 'async_mode': 'eventlet'}),
    jsglue
]
