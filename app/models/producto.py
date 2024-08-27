from app import db
from datetime import datetime
from sqlalchemy import Numeric

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    precio = db.Column(Numeric(10), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    colores = db.Column(db.String(50), nullable=True)
    imagen = db.Column(db.String(255))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=True)
    genero = db.Column(db.String(10))
    tipo = db.Column(db.String(10))
    tallas = db.Column(db.String(200)) 
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow) 


    pedido_item = db.relationship('PedidoItem', back_populates='producto', lazy=True)
    inventario = db.relationship('Inventario', back_populates='producto', lazy=True)
    categoria = db.relationship('Categoria', back_populates='productos')
