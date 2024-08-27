from app import db

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=True)
    genero = db.Column(db.String(10), nullable=False)


    productos = db.relationship('Producto', back_populates='categoria')