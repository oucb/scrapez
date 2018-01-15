from flask import Flask
from flask_jsglue import JSGlue
from apps.ui.blueprints import BLUEPRINTS
from apps.ui.extensions import EXTENSIONS
import os
import logging
from config import config
# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

def create_app(profile=None):
    if profile is None:
        profile = os.environ.get('PROFILE', 'default')
    log.info("Current profile is '%s'" % profile)
    cfg = config[profile]
    app = Flask(__name__)
    app.config.from_object(cfg)
    JSGlue(app)
    register_extensions(app, EXTENSIONS)
    register_blueprints(app, BLUEPRINTS)
    return app

def register_blueprints(app, blueprints):
    """Register all Flask blueprints with our Flask app.

    Args:
        app: The Flask application.
        blueprints (list): A list of tuple (blueprint, path).
    """
    for bp, path in blueprints:
        try:
            app.register_blueprint(bp, url_prefix=path)
            log.info("Blueprint registered: %s --> %s" % (bp, path))
        except Exception as e:
            log.error("Error registering blueprint %s --> %s" % (bp, path))
    log.debug("Registered %s blueprints" % len(blueprints))
    log.info("URL Map: %s" % app.url_map)

def register_extensions(app, extensions):
    """Register all Flask extensiosn with our Flask app.

    Args:
        app: The Flask application.
        extensions (list): A list of extensions.
    """
    for extension in extensions:
        try:
            extension.init_app(app)
            log.info("Extension registered: %s" % extension.__class__.__name__)
        except Exception as e:
            log.error("Error registering extension %s" % extension.__class__.__name__)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, threaded=True)
