from flask import Blueprint

videos = Blueprint('videos', __name__)

import routes, events
