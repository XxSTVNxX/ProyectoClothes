from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import producto_routes, categoria_routes, carrito_routes, auth_routes, pedido_routes, proveedor_routes, inventario_routes

    app.register_blueprint(producto_routes.bp)
    app.register_blueprint(categoria_routes.bp)
    app.register_blueprint(carrito_routes.bp)
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(pedido_routes.bp)
    app.register_blueprint(proveedor_routes.bp)
    app.register_blueprint(inventario_routes.bp)
    # Cargar el modelo Cliente dentro de la función user_loader para evitar el problema de importación circular.
    from app.models import Cliente

    @login_manager.user_loader
    def load_user(user_id):
        return Cliente.query.get(int(user_id))

    return app
