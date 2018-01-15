from flask import session
from flask_socketio import emit, join_room, leave_room
from apps.ui.extensions import socketio

@socketio.on('list_downloads', namespace='/download')
def list_downloads(message):
    """List files on local drive and emit 'file_found' event."""
    items = []
    for filename in os.listdir(app.config['DOWNLOAD_FOLDER']):
        extension = filename.split('.')[-1]
        if extension in ['mp4', 'avi']:
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
            download_url = url_for('downloads.send_file', filename=filename)
            item = {
                'filename': filename,
                'download_url': download_url
            }
            emit('file_found', item, namespace='/download')
