from flask_script import Manager, Server
from scrapez.ui import create_app
from scrapez.ui.extensions import socketio
from flask_flash.extensions import db
from flask_script import Shell
from flask_migrate import Migrate
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
migrate = Migrate(app, db)

def make_shell_context():
    from scrapez.api import models
    return dict(app=app, db=db, models=models)

# Manager commands
manager.add_command("shell", Shell(make_context=make_shell_context))
@manager.command
def runserver():
    try:
        app_type = app.config['FLASK_APP']
        if app_type == 'ui':
            socketio.run(app,
                         host='127.0.0.1',
                         port=5000,
                         use_reloader=app.config['DEBUG'],
                         log_output=True)
        elif app_type == 'api':
            app.run(host='127.0.0.1', port=5001, use_reloader=app.config['DEBUG'])
        else:
            raise Exception("%s not known" % app_type)
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
