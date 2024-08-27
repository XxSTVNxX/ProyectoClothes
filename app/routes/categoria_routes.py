from flask import Blueprint, request, redirect, url_for, render_template
from app import db
from app.models.categoria import Categoria

bp = Blueprint('categoria', __name__)

@bp.route('/categoria', methods=['GET'])
def index():
    data = Categoria.query.all()
    return render_template('categoria/index.html', data=data)

@bp.route('/categoria/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        genero = request.form['genero']

        if not nombre:
            # Aquí puedes agregar manejo de errores
            return render_template('categoria/add.html', error='El nombre es requerido.')
        
        if not genero:
            # Aquí puedes agregar manejo de errores
            return render_template('categoria/add.html', error='El genero es requerido.')

        newCategory = Categoria(nombre=nombre, genero=genero)
        db.session.add(newCategory)
        db.session.commit()
        return redirect(url_for('categoria.index'))
    return render_template('categoria/add.html')

@bp.route('/categoria/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')

        if not nombre:
            return render_template('categoria/edit.html', categoria=categoria, error='El nombre es requerido.')

        categoria.nombre = nombre
        db.session.commit()
        return redirect(url_for('categoria.index'))
    return render_template('categoria/edit.html', categoria=categoria)

@bp.route('/categoria/delete/<int:id>')
def delete(id):
    category = Categoria.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categoria.index'))
