from flask_flash import Flash
from api import Result

def create_app(type):
    if type == 'api':
        app = Flash(
            resources=[
                Result
            ],
            port=5001
        )
        return app
