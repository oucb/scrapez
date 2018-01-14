from flask_script import Manager, Server
from apps import create_app
import logging

log = logging.getLogger(__name__)

app = create_app()
manager = Manager(app)

class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        return Server.__call__(self, app, *args, **kwargs)

server = CustomServer(host="0.0.0.0", port=5000)
manager.add_command("runserver", server)

if __name__ == '__main__':
    try:
        manager.run()
    except Exception as e:
        log.exception(e)
    except KeyboardInterrupt:
        sys.exit()
