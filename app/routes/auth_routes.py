from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.cliente import Cliente
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Cliente.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('producto.index'))
        else:
            flash('Email o contraseña inválidos')

    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        password = request.form['password']

                # Verificar si el correo ya existe
        user = Cliente.query.filter_by(email=email).first()
        if user:
            flash('El correo ya existe.', 'error')
            return redirect(url_for('auth.register'))

        user = Cliente(
            email=email,
            nombre=nombre,
            apellido=apellido,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )

        db.session.add(user)
        db.session.commit()

        flash('Registro exitoso. Por favor, inicia sesión.', 'success')
        login_user(user)
        return redirect(url_for('producto.index'))

    return render_template('auth/register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
