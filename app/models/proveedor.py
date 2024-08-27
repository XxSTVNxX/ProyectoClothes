from app import db

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), nullable=True)

    productos = db.relationship('Inventario', backref='proveedor', lazy=True)

    
