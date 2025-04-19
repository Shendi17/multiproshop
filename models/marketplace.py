from app import db

class Marketplace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=True)
    products = db.relationship('Product', backref='marketplace', lazy=True)
