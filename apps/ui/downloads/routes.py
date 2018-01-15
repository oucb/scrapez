from . import downloads
from flask import send_from_directory, current_app as app, url_for
import os

@downloads.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

@downloads.route('/list')
def list_downloads():
    items = []
    for file in os.listdir(app.config['DOWNLOAD_FOLDER']):
        ext = file.split('.')[-1]
        if ext not in ['mp4', 'avi']:
            path = os.path.join(app.config['DOWNLOAD_FOLDER'], file)
            download_url = url_for('downloads.send_file', filename=path)
            item = {
                'path': path,
                'download_url': download_url
            }
            items.append(path)
    return jsonify({
        'downloads': items
    })
