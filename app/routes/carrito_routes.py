from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.pedidoItem import PedidoItem
from app.models.envio import Envio
from app import db

bp = Blueprint('carrito', __name__)

@bp.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    productos = []
    for item in carrito:
        producto = Producto.query.get(item['producto_id'])
        if producto:
            productos.append({
                'producto': producto,
                'cantidad': item['cantidad'],
                'talla': item.get('talla'),
                'color': item.get('color')
            })
    return render_template('carrito/ver.html', productos=productos)

@bp.route('/carrito/agregar/<int:producto_id>', methods=['POST'])
def agregar_al_carrito(producto_id):
    cantidad = int(request.form.get('cantidad', 1))
    talla = request.form.get('talla')
    color = request.form.get('color')

    # Verificar que los datos se recibieron correctamente
    print(f"Producto ID: {producto_id}, Cantidad: {cantidad}, Talla: {talla}, Color: {color}")

    carrito = session.get('carrito', [])

    # Verifica si el producto ya está en el carrito con la misma talla y color
    for item in carrito:
        if (item.get('producto_id') == producto_id and
            item.get('talla') == talla and
            item.get('color') == color):
            item['cantidad'] += cantidad
            break
    else:
        # Si no está, lo agrega al carrito
        carrito.append({
            'producto_id': producto_id,
            'cantidad': cantidad,
            'talla': talla,
            'color': color
        })

    # Actualiza la sesión con el nuevo carrito
    session['carrito'] = carrito
    flash('Producto agregado al carrito.')
    return redirect(url_for('carrito.ver_carrito'))


@bp.route('/carrito/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        identificacion = request.form.get('identificacion')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')

        # Crear el pedido con la información del cliente
        nuevo_pedido = Pedido(
            nombre_cliente=nombre,
            apellido_cliente=apellido,
            email_cliente=email,
            identificacion=identificacion,
            direccion_cliente=direccion,
            telefono_cliente=telefono,
            estado=None
        )
        db.session.add(nuevo_pedido)
        db.session.commit()

        carrito = session.get('carrito', [])
        for item in carrito:
            producto = Producto.query.get(item['producto_id'])
            if producto:
                pedido_item = PedidoItem(
                    producto_id=producto.id,
                    pedido_id=nuevo_pedido.id,
                    cantidad=item['cantidad'],
                    talla=item.get('talla'),
                    color=item.get('color')
                )
                db.session.add(pedido_item)
        db.session.commit()

        # Crear el registro de envío
        nuevo_envio = Envio(pedido_id=nuevo_pedido.id)
        db.session.add(nuevo_envio)
        db.session.commit()

        # Limpiar el carrito de la sesión después del pedido
        session.pop('carrito', None)
        flash('Pedido realizado con éxito.')
        return redirect(url_for('producto.index'))

    return render_template('carrito/checkout.html')

@bp.route('/carrito/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_del_carrito(producto_id):
    carrito = session.get('carrito', [])
    nuevo_carrito = [item for item in carrito if item['producto_id'] != producto_id]

    session['carrito'] = nuevo_carrito
    flash('Producto eliminado del carrito.')
    return redirect(url_for('carrito.ver_carrito'))
