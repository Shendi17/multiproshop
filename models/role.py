from app import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Exemple: 'client', 'vendeur', 'admin'
    description = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy=True)
