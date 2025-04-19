from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from datetime import datetime

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'votre_clé_secrète_ici')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///boutique.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    # Créer les dossiers nécessaires
    os.makedirs(os.path.join(app.root_path, 'static', 'images'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'templates', 'auth'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'templates', 'products'), exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'templates', 'cart'), exist_ok=True)

    # Initialiser les extensions avec l'application
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import des modèles
    from models.user import User
    from models.product import Product
    from models.category import Category
    from models.order import Order, OrderItem

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Créer les tables
    with app.app_context():
        db.create_all()

    # Context processor pour les variables globales
    @app.context_processor
    def inject_global_vars():
        return {
            'now': datetime.utcnow(),
            'categories': Category.query.all()
        }

    # Enregistrer les blueprints
    from routes.main import main as main_blueprint
    from routes.auth import auth as auth_blueprint
    from routes.products import products as products_blueprint
    from routes.cart import cart as cart_blueprint
    from routes.supplier import supplier_blueprint
    from routes.marketplace import marketplace_blueprint
    from routes.video import video_blueprint
    from routes.ai import ai_blueprint
    from routes.api import api_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(products_blueprint, url_prefix='/products')
    app.register_blueprint(cart_blueprint, url_prefix='/cart')
    app.register_blueprint(supplier_blueprint, url_prefix='/suppliers')
    app.register_blueprint(marketplace_blueprint, url_prefix='/marketplaces')
    app.register_blueprint(video_blueprint, url_prefix='/videos')
    app.register_blueprint(ai_blueprint, url_prefix='/ai')
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route('/multiproshop/')
    def multiproshop_root():
        return redirect(url_for('index'))  # Redirige vers la page d'accueil principale

    return app

# Créer l'application
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
