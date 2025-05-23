from extensions import db
from models.user import User
from models.role import Role
from app import app

def run():
    with app.app_context():
        # Création du rôle admin s'il n'existe pas
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrateur du site')
            db.session.add(admin_role)
            db.session.commit()

        # Création de l'utilisateur admin s'il n'existe pas
        admin_user = User.query.filter_by(email='admin@multiproshop.com').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@multiproshop.com',
                role=admin_role
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
        print('Admin prêt !')

if __name__ == '__main__':
    run()
