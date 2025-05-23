from extensions import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), nullable=False)
    title = db.Column(db.String(128))
    description = db.Column(db.Text)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
