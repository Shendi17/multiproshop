from extensions import db
from datetime import datetime
from .video import Video

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    brand = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Ajouts avancés
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    marketplace_id = db.Column(db.Integer, db.ForeignKey('marketplace.id'))
    videos = db.relationship('Video', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'
