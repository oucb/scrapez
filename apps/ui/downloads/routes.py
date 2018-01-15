from . import downloads
from flask import send_from_directory, current_app as app, url_for, jsonify
import os

EXTENSIONS_WHITELIST = [
    'mp4',
    'avi',
    'pdf'
]
EXTENSIONS_BLACKLIST = [
    'exe',
    'sh',
    'o',
    'dll',\
    'torrent'
]

@downloads.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

@downloads.route('/list')
def list_downloads():
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
            items.append(item)
    return jsonify({
        'downloads': items
    })
