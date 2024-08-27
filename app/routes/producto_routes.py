# routes/producto_routes.py
from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from flask_login import current_user, login_required
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.inventario import Inventario
from decimal import Decimal
from werkzeug.utils import secure_filename
import os

from app import db

from app import db

bp = Blueprint('producto', __name__)

@bp.route('/')
def index():
    productos = Producto.query.all()
    categorias = Categoria.query.all()    # Obtén los filtros desde la URL (GET parameters)
    categoria_id = request.args.get('categoria')
    genero = request.args.get('genero')
    tipo = request.args.get('tipo')
    color = request.args.get('color')
    talla = request.args.get('talla')

    # Construir la consulta base
    query = Producto.query

    # Aplicar filtros
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    if genero:
        query = query.filter_by(genero=genero)
    if tipo:
        query = query.filter_by(tipo=tipo)
    if color:
        query = query.filter(Producto.colores.contains(color))
    if talla:
        query = query.filter(Producto.tallas.contains(talla))

    # Ejecutar la consulta
    productos = query.all()

    return render_template('zay/shop.html', productos=productos, categorias=categorias)
    # Renderizar la plantilla con los productos filtrados


@bp.route('/producto/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        stock = request.form.get('stock', 0)
        descripcion = request.form['descripcion']
        precio_str = request.form['precio'].replace('.', '').replace(',', '.')
        precio = Decimal(precio_str)
        categoria_id = request.form['categoria_id']
        genero = request.form['genero']
        tipo = request.form['tipo']
        tallas = request.form.getlist('tallas') 
        colores = request.form.getlist('colores') 

        imagen = request.files['imagen']
        

        if imagen:
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join('static', 'images', filename)
            imagen.save(os.path.join(os.path.dirname(__file__), '..', imagen_path))
            ruta_imagen = imagen_path

        else:
            imagen=None

        categoria = Categoria.query.get(categoria_id)
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            stock=int(stock),
            precio=precio,
            categoria=categoria,
            genero=genero,
            tipo=tipo,
            colores=','.join(colores),
            tallas=','.join(tallas),
            imagen=imagen.filename 

        )
        db.session.add(nuevo_producto)
        db.session.commit()

        nuevo_inventario = Inventario(
            producto_id=nuevo_producto.id,
        )
        db.session.add(nuevo_inventario)
        db.session.commit()
        
        return redirect(url_for('producto.index'))
        

    categorias = Categoria.query.all()
    return render_template('producto/add.html', categorias=categorias)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        # Actualizar los detalles del producto con los datos del formulario
        producto.nombre = request.form.get('nombre')
        producto.stock = int(request.form.get('stock'))  # Obtener el stock del formulario y convertirlo a entero
        producto.descripcion = request.form.get('descripcion')
        producto.precio = float(request.form.get('precio'))
        producto.tipo = request.form.get('tipo')
        producto.genero = request.form.get('genero')
        producto.tallas = request.form.get('tallas')
        producto.colores = request.form.get('colores')

        # Procesar la imagen
        imagen = request.files.get('imagen')

        if imagen:
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join('static', 'images', filename)
            imagen.save(os.path.join(os.path.dirname(__file__), '..', imagen_path))
            ruta_imagen = imagen_path


        categoria_id = request.form['categoria']
        
        producto.categoria = Categoria.query.get(categoria_id)

        # Guardar los cambios en la base de datos
        db.session.commit()
        flash('Producto actualizado correctamente.')
        db.session.commit()
        return redirect(url_for('producto.index'))

    categorias = Categoria.query.all()
    return render_template('producto/edit.html', producto=producto, categorias=categorias)

# routes/producto_routes.py

@bp.route('/detalle/<int:id>', methods=['GET', 'POST'])
def detalle(id):
    producto = Producto.query.get_or_404(id)

    tallas = []
    tallas = producto.tallas.split(',') if producto.tallas else []
    
    colores = []
    colores = producto.colores.split(',') if producto.colores else []

    return render_template('zay/detalle.html', producto=producto, tallas=tallas, colores=colores)

@bp.route('/producto/delete/<int:id>', methods=['POST'])
def delete(id):
    # Buscar el producto por ID
    producto = Producto.query.get_or_404(id)
    
    try:
        # Eliminar el producto de cualquier inventario asociado
        inventario = Inventario.query.filter_by(producto_id=id).first()
        if inventario:
            db.session.delete(inventario)
        
        # Eliminar el producto en sí
        db.session.delete(producto)
        db.session.commit()
        
        flash('Producto eliminado correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Hubo un error al eliminar el producto: {}'.format(str(e)), 'danger')
    
    return redirect(url_for('producto.index'))

@bp.route('/productos')
def listar_productos():
    categorias = Categoria.query.all()
    categoria_id = request.args.get('categoria_id')
    genero = request.args.get('genero')
    tipo = request.args.get('tipo')
    color = request.args.get('color')
    talla = request.args.get('talla')

    # Construir la consulta base
    query = Producto.query

    # Aplicar filtros
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    if genero:
        query = query.filter_by(genero=genero)
    if tipo:
        query = query.filter_by(tipo=tipo)
    if color:
        query = query.filter(Producto.colores.contains(color))
    if talla:
        query = query.filter(Producto.tallas.contains(talla))

    # Ejecutar la consulta
    productos = query.all()

    return render_template('producto/listar.html', productos=productos, categorias=categorias)

@bp.route('/productos/buscar')
def buscar_productos():
    query = request.args.get('q')
    productos = Producto.query.filter(Producto.nombre.contains(query) | Producto.descripcion.contains(query)).all()
    return render_template('producto/listar.html', productos=productos)


