from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.proveedor import Proveedor

bp = Blueprint('proveedor', __name__)

# Listar todos los proveedores
@bp.route('/proveedores')
def index():
    proveedores = Proveedor.query.all()
    return render_template('proveedor/index.html', proveedores=proveedores)

# Agregar un nuevo proveedor
@bp.route('/proveedores/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        if Proveedor.query.filter_by(email=email).first():
            flash('Ya existe un proveedor con ese email.')
            return redirect(url_for('proveedor.add'))

        nuevo_proveedor = Proveedor(
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion
        )
        db.session.add(nuevo_proveedor)
        db.session.commit()
        flash('Proveedor agregado exitosamente.')
        return redirect(url_for('proveedor.index'))
    
    return render_template('proveedor/add.html')

# Editar un proveedor existente
@bp.route('/proveedores/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    proveedor = Proveedor.query.get_or_404(id)

    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.email = request.form['email']
        proveedor.telefono = request.form['telefono']
        proveedor.direccion = request.form['direccion']
        
        db.session.commit()
        flash('Proveedor actualizado exitosamente.')
        return redirect(url_for('proveedor.index'))
    
    return render_template('proveedor/edit.html', proveedor=proveedor)

# Eliminar un proveedor
@bp.route('/proveedores/delete/<int:id>', methods=['POST'])
def delete(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado exitosamente.')
    return redirect(url_for('proveedor.index'))

