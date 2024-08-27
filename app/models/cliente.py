from app import db
from flask_login import UserMixin

class Cliente(db.Model, UserMixin):
    __tablename__ = 'cliente'
    
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    Rol = db.Column(db.String(20), nullable=False, default='usuario')
    

