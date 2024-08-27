
from app import db

class CarritoItem(db.Model):
    __tablename__ = 'carrito_item'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    carrito_id = db.Column(db.Integer, db.ForeignKey('carrito.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    producto = db.relationship('Producto')