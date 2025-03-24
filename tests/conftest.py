import pytest
from app import create_app, db
from datetime import datetime, timedelta
from app.models.stock import Stock, StockPrice

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


# Test data helpers

def create_stock(app, symbol="TST", name="Test Co", founded="2020-01-01", description="Test stock"):
    with app.app_context():
        stock = Stock(
            name=name,
            symbol=symbol,
            founded=datetime.strptime(founded, "%Y-%m-%d").date(),
            description=description
            )
        db.session.add(stock)
        db.session.commit()
        return stock.id

def create_prices(app, stock_id, start_price=100.0, step=1, days=10, start_date="2022-01-01"):
    with app.app_context():
        base_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        prices = [
            StockPrice(date=base_date + timedelta(days=i), close=start_price + i * step, stock_id=stock_id)
            for i in range(days)
        ]
        db.session.add_all(prices)
        db.session.commit()