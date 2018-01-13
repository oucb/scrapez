from flask import Flask
from blueprints import BLUEPRINTS
import os
import logging
# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

def create_app():
    app = Flask(__name__)
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

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
