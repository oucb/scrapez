from flask_flash.extensions import db, ma

class DownloadModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    path = db.Column(db.Text)
    size = db.Column(db.Integer)
    extra_data = db.Column(db.Text)

class DownloadSchema(ma.ModelSchema):
    class Meta:
        model = DownloadModel
    title = ma.Field(required=True)
    url = ma.Field(required=True)
    path = ma.Field(required=True)
    size = ma.Field(required=True)
