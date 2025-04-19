from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from app import db

auth = Blueprint('auth', __name__)

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
    
    return render_template('auth/register.html')

@auth.route('/connexion', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Identifiants invalides')
    
    return render_template('auth/login.html')

@auth.route('/deconnexion')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/profil')
@login_required
def profile():
    return render_template('auth/profile.html')
