from app import db


class Inventario(db.Model):
    __tablename__ = 'inventario'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=True)

    producto = db.relationship('Producto', back_populates='inventario', lazy=True)
