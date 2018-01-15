from . import downloads
from flask import send_from_directory, current_app as app

@downloads.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)
