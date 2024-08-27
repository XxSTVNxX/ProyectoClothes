from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.pedido import Pedido
from app.models.pedidoItem import PedidoItem
from app.models.envio import Envio
from app import db

bp = Blueprint('pedido', __name__)

@bp.route('/pedidos')
def listar_pedidos():
    pedidos = Pedido.query.filter(Pedido.estado.is_(None)).all()

    # Verifica que los pedidos se están recuperando correctamente
    print(f'Pedidos pendientes encontrados: {len(pedidos)}')
    for pedido in pedidos:
        print(f'Pedido ID: {pedido.id}, Estado: {pedido.estado}') # Debugging: Detalle de cada pedido encontrado
    return render_template('pedido/index.html', pedidos=pedidos)

@bp.route('/pedidos/<int:id>')
def ver_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    items = PedidoItem.query.filter_by(pedido_id=pedido.id).all()
    envio = Envio.query.filter_by(pedido_id=pedido.id).first()
    return render_template('pedido/detalle.html', pedido=pedido, items=items, envio=envio)

@bp.route('/pedido/completar/<int:id>', methods=['POST'])
def marcar_completado(id):
    pedido = Pedido.query.get_or_404(id)
    pedido.estado = 'completado'  # Asegúrate de tener un campo `estado` en tu modelo Pedido
    db.session.commit()
    flash('El pedido ha sido marcado como completado.')
    return redirect(url_for('pedido.listar_pedidos'))

@bp.route('/pedido/cancelar/<int:id>', methods=['POST'])
def cancelar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    pedido.estado = 'cancelado'  # Asegúrate de tener un campo `estado` en tu modelo Pedido
    db.session.commit()
    flash('El pedido ha sido cancelado.')
    return redirect(url_for('pedido.listar_pedidos'))

@bp.route('/pedidos/completados')
def pedidos_completados():
    pedidos = Pedido.query.filter_by(estado='completado').all()
    return render_template('pedido/completado.html', pedidos=pedidos)

@bp.route('/pedidos/cancelados')
def pedidos_cancelados():
    pedidos = Pedido.query.filter_by(estado='cancelado').all()
    return render_template('pedido/cancelado.html', pedidos=pedidos)
@bp.route('/pedidos/enviar/<int:id>', methods=['POST'])
def marcar_envio(id):
    pedido = Pedido.query.get_or_404(id)
    envio = Envio.query.filter_by(pedido_id=pedido.id).first()

    if not envio:
        envio = Envio(pedido_id=pedido.id, estado="Enviado")
        db.session.add(envio)
    else:
        envio.estado = "Enviado"
    
    db.session.commit()
    flash('Pedido marcado como enviado.')
    return redirect(url_for('pedido.ver_pedido', id=id))

@bp.route('/pedido/restaurar/<int:id>', methods=['POST'])
def restaurar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    pedido.estado = None
    db.session.commit()
    flash('Pedido restaurado al estado pendiente.')
    return redirect(request.referrer)

