from flask_sslify import SSLify
from flask import Flask
from config import config
from ..utils import register_blueprints, register_extensions
import os

def create_app(profile=None, ssl=False):
    if profile is None:
        profile = os.environ.get('PROFILE', 'default')
    cfg = config[profile]
    app = Flask(__name__)
    if ssl:
        SSLify(app)
    app.config.from_object(cfg)
    app.url_map.strict_slashes = False

    from blueprints import BLUEPRINTS
    register_blueprints(app, BLUEPRINTS)

    from extensions import EXTENSIONS
    register_extensions(app, EXTENSIONS)

    return app
