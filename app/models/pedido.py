from app import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    nombre_cliente = db.Column(db.String(100), nullable=False)
    apellido_cliente = db.Column(db.String(100), nullable=False)
    email_cliente = db.Column(db.String(120), nullable=False)
    direccion_cliente = db.Column(db.String(200), nullable=False)
    telefono_cliente = db.Column(db.String(20), nullable=False)
    fecha_pedido = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    identificacion = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(20), nullable=True, default=None)

    items = db.relationship('PedidoItem', back_populates='pedido', lazy=True)
    envio = db.relationship('Envio', backref='envio',uselist=False)



