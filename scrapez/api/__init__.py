from flask_flash import Flash
from flask_sslify import SSLify
from extensions import EXTENSIONS
from config import config
from resources import Download
from config import config
import os

def create_app(profile=None, ssl=False):
    if profile is None:
        profile = os.environ.get('PROFILE', 'default')
    flash = Flash(
        resources=[Download],
        config=config,
        profile=profile,
        extensions=EXTENSIONS)
    app = flash.app
    if ssl:
        SSLify(app)
    return app
