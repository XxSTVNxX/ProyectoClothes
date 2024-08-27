from app import db

class Envio(db.Model):
    __tablename__ = 'envio'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    estado = db.Column(db.String(20), default='Pendiente')
