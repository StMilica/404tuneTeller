from app import db
from app.models.stock import Stock
from app.models.stock_price import StockPrice
from datetime import datetime, timedelta

def create_sample_stock():
    return Stock(
        name="Test Corp",
        symbol="TST",
        founded=datetime(2020, 1, 1).date(),
        description="Test stock"
    )

def create_sample_prices(stock_id, start_price=100.0):
    prices = []
    date = datetime(2020, 1, 1).date()
    for i in range(10):
        prices.append(
            StockPrice(
                date=date + timedelta(days=i),
                close=start_price + i,
                stock_id=stock_id
            )
        )
    return prices

def create_test_stock_with_prices(app, symbol="TST"):
    with app.app_context():
        stock = Stock(
            name="Test Stock",
            symbol=symbol,
            founded=datetime(2022, 1, 1).date()
        )
        db.session.add(stock)
        db.session.commit()

        base_date = datetime(2022, 1, 1).date()
        prices = [
            StockPrice(date=base_date + timedelta(days=i), close=100 + i, stock_id=stock.id)
            for i in range(10)
        ]
        db.session.add_all(prices)
        db.session.commit()

def test_profit_endpoint(client, app):
    with app.app_context():
        stock = create_sample_stock()
        db.session.add(stock)
        db.session.commit()

        prices = create_sample_prices(stock.id)
        db.session.add_all(prices)
        db.session.commit()

    response = client.get("/api/stocks/TST/profit?start=2020-01-01&end=2020-01-05")
    assert response.status_code == 200
    data = response.get_json()
    assert "main_range" in data
    assert data["main_range"]["best_trade"]["profit"] > 0
    assert data["stock"] == "TST"

def test_get_prices_from_db(client, app):
    with app.app_context():
        stock = Stock(name="Test", symbol="TST", founded=datetime(2020,1,1).date())
        db.session.add(stock)
        db.session.commit()

        price = StockPrice(date=datetime(2020,1,2).date(), close=150.0, stock_id=stock.id)
        db.session.add(price)
        db.session.commit()

    response = client.get("/api/db/stocks/TST/prices")
    assert response.status_code == 200
    data = response.get_json()
    assert data["stock"] == "TST"
    assert len(data["prices"]) == 1
    assert data["prices"][0]["close"] == 150.0

def test_profit_route_valid(client, app):
    create_test_stock_with_prices(app)

    response = client.get("/api/stocks/TST/profit?start=2022-01-01&end=2022-01-05")
    assert response.status_code == 200

    data = response.get_json()
    assert data["stock"] == "TST"
    assert "main_range" in data
    assert "best_trade" in data["main_range"]
    assert data["main_range"]["best_trade"]["profit"] > 0
    assert data["main_range"]["total_profit"] > 0

def test_profit_route_missing_query(client):
    response = client.get("/api/stocks/TST/profit")
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_profit_route_invalid_date(client):
    response = client.get("/api/stocks/TST/profit?start=bad-date&end=2022-01-05")
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_profit_route_unknown_stock(client):
    response = client.get("/api/stocks/UNKNST/profit?start=2022-01-01&end=2022-01-05")
    assert response.status_code == 404
    assert "error" in response.get_json()