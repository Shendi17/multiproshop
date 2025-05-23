from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from extensions import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/inscription', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Un utilisateur avec ce nom ou cet email existe déjà')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Inscription réussie. Connectez-vous!')
        return redirect(url_for('auth.login'))
    
    return render_template('pages/register.html')

@auth.route('/connexion', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifiant = request.form.get('username')
        password = request.form.get('password')

        # Permet la connexion avec username OU email
        user = User.query.filter((User.username == identifiant) | (User.email == identifiant)).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Identifiants invalides')
    return render_template('pages/login.html')

@auth.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        identifiant = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter((User.username == identifiant) | (User.email == identifiant)).first()
        if user and user.check_password(password):
            if getattr(user.role, 'name', None) == 'admin':
                login_user(user)
                return redirect(url_for('admin.dashboard'))
            else:
                flash("Accès réservé aux administrateurs.")
        else:
            flash('Identifiants invalides')
    return render_template('pages/admin_login.html')

@auth.route('/deconnexion')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/profil')
@login_required
def profile():
    return render_template('pages/profile.html')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Ici tu pourrais envoyer un email de réinitialisation si tu as une logique d'envoi de mail
        flash("Si un compte existe pour cet email, un lien de réinitialisation a été envoyé.")
        return redirect(url_for('auth.login'))
    return render_template('pages/forgot_password.html')
