from extensions import db

class ApiIntegration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    api_key = db.Column(db.String(256))
    api_url = db.Column(db.String(256))
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
