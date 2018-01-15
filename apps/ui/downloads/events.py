from flask import session, url_for
from flask_socketio import emit
from apps.ui.extensions import socketio
import logging
import os

log = logging.getLogger(__name__)

@socketio.on('list_files', namespace='/download')
def list_files(message):
    """List files on local drive and emit 'file_found' event."""
    log.info("List downloads from drive")
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
            log.info("Found download: %s" % item)
            emit('new_file', item, namespace='/download')
