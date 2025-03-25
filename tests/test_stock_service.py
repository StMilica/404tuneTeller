import pytest
from app import db
from app.models.stock import Stock
from app.services.stock_service import StockService
from datetime import datetime

@pytest.fixture
def stock_service():
    return StockService()

def test_list_stocks_empty(app, stock_service):
    with app.app_context():
        result = stock_service.list_stocks()
        assert result == []

def test_create_and_list_stocks(app, stock_service):
    with app.app_context():
        stock = Stock(name="Apple", symbol="AAPL", founded=datetime(1976, 4, 1).date(), description="Tech")
        stock_service.create_stock(stock)
        result = stock_service.list_stocks()
        assert len(result) == 1
        assert result[0].symbol == "AAPL"

def test_get_stock(app, stock_service):
    with app.app_context():
        stock = Stock(name="Test", symbol="TST", founded=datetime(2020, 1, 1).date(), description="Test")
        db.session.add(stock)
        db.session.commit()
        found = stock_service.get_stock(stock.id)
        assert found.symbol == "TST"
        missing = stock_service.get_stock(999)
        assert missing is None

def test_update_stock(app, stock_service):
    with app.app_context():
        stock = Stock(name="Old", symbol="OLD", founded=datetime(2010, 1, 1).date())
        db.session.add(stock)
        db.session.commit()

        updated = stock_service.update_stock(stock.id, {
            "name": "New Name",
            "symbol": "NEW",
            "description": "Updated"
        })
        assert updated.name == "New Name"
        assert updated.symbol == "NEW"
        assert updated.description == "Updated"

        none_result = stock_service.update_stock(999, {"name": "None"})
        assert none_result is None

def test_delete_stock(app, stock_service):
    with app.app_context():
        stock = Stock(name="DeleteMe", symbol="DEL", founded=datetime(2020, 1, 1).date())
        db.session.add(stock)
        db.session.commit()

        deleted = stock_service.delete_stock(stock.id)
        assert deleted is True
        assert stock_service.get_stock(stock.id) is None

        missing = stock_service.delete_stock(999)
        assert missing is False
