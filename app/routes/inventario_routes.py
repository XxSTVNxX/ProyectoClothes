from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.inventario import Inventario
from app.models.proveedor import Proveedor

bp = Blueprint('inventario', __name__)
@bp.route('/inventario')
def ver_inventario():
    inventarios = Inventario.query.all()
    proveedores = Proveedor.query.all()
    return render_template('inventario/index.html', inventarios=inventarios, proveedores=proveedores)


@bp.route('/inventario/actualizar_proveedor/<int:inventario_id>', methods=['POST'])
def actualizar_proveedor(inventario_id):
    inventario = Inventario.query.get_or_404(inventario_id)
    proveedor_id = request.form.get('proveedor_id')

    if proveedor_id:
        proveedor = Proveedor.query.get(proveedor_id)
        if proveedor:
            inventario.proveedor_id = proveedor.id
            db.session.commit()
            flash('Proveedor actualizado correctamente.')
        else:
            flash('Proveedor no encontrado.')
    else:
        flash('Debe seleccionar un proveedor.')

    return redirect(url_for('inventario.ver_inventario'))

@bp.route('/inventario/editar_proveedor/<int:inventario_id>', methods=['GET', 'POST'])
def editar_proveedor(inventario_id):
    inventario = Inventario.query.get_or_404(inventario_id)
    
    if request.method == 'POST':
        proveedor_id = request.form.get('proveedor_id')
        
        if proveedor_id:
            proveedor = Proveedor.query.get(proveedor_id)
            if proveedor:
                inventario.proveedor_id = proveedor.id
                db.session.commit()
                flash('Proveedor actualizado correctamente.')
            else:
                flash('Proveedor no encontrado.')
        else:
            flash('Debe seleccionar un proveedor.')
            
        return redirect(url_for('inventario.ver_inventario'))
    
    proveedores = Proveedor.query.all()
    return render_template('inventario/edit.html', inventario=inventario, proveedores=proveedores)
