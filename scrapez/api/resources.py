from flask_flash import CRUD
from models import DownloadModel, DownloadSchema

class Download(CRUD):
    model = DownloadModel
    schema = DownloadSchema
