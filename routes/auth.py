from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    
    # Rota para registro de novos usuários.
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica se o usuário ou email já existem
        existing_user = Usuario.query.filter_by(username=username).first()
        existing_email = Usuario.query.filter_by(email=email).first()

        if existing_user:
            flash('Nome de usuário já existe. Por favor, escolha outro.', 'danger')
            return render_template('auth/register.html')
        if existing_email:
            flash('Email já registrado. Por favor, faça login ou use outro email.', 'danger')
            return render_template('auth/register.html')

        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = Usuario(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registro realizado com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    # Rota para login de usuários.
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Usuario.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next') # Redireciona para a página anterior, se houver
            return redirect(next_page or url_for('dashboard.dashboard'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():

    # Rota para logout de usuários.

    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))
