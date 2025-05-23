from extensions import db

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    contact_email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    website = db.Column(db.String(256))
    api_url = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=True)
    products = db.relationship('Product', backref='supplier', lazy=True)
