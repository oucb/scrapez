from flask_flash.extensions import db, ma

class DownloadModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    path = db.Column(db.Text)

class DownloadSchema(ma.ModelSchema):
    class Meta:
        model = DownloadModel
    name = ma.Field(required=True)
    path = ma.Field(required=True)
