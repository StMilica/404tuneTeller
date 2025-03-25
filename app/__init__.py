from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///404tuneTeller.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.stock_routes import stock_routes
    from app.routes.health_routes import health_routes

    app.register_blueprint(stock_routes)
    app.register_blueprint(health_routes)

    return app