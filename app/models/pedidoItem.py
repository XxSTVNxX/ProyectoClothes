from app import db

class PedidoItem(db.Model):
    __tablename__ = 'pedido_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cantidad = db.Column(db.Integer, nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id', ondelete='CASCADE'))
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    talla = db.Column(db.String(10), nullable=True)
    color = db.Column(db.String(20), nullable=True)

    pedido = db.relationship('Pedido', back_populates='items', lazy=True)
    producto = db.relationship('Producto', back_populates='pedido_item')



