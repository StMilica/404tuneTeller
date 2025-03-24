from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from app.routes import stock_routes
    app.register_blueprint(stock_routes)

    return app