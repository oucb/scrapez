from . import create_app
import models
from flask_migrate import Migrate
from flask_flash import db

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, models=models)
