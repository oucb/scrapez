from flask_script import Manager, Server
from apps import create_app
from apps.ui.extensions import socketio
import config
import logging
import sys

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    filename="ui.log",
                    format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
                    handlers=[logging.StreamHandler()])

app = create_app()
manager = Manager(app)

@manager.command
def run():
    try:
        socketio.run(app,
                     host='127.0.0.1',
                     port=5000,
                     use_reloader=False,
                     log_output=True)
    except Exception as e:
        log.exception(e)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    try:
        manager.run()
    except Exception as e:
        log.exception(e)
    except KeyboardInterrupt:
        sys.exit()
