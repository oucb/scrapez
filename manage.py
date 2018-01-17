from flask_script import Manager, Server
from apps import create_app
from apps.ui.extensions import socketio
import config
import sys

app = create_app()
log = app.logger
manager = Manager(app)

class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        return Server.__call__(self, app, *args, **kwargs)

server = CustomServer(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)

@manager.command
def run():
    try:
        socketio.run(app,
                     host='127.0.0.1',
                     port=5000,
                     use_reloader=False)
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
