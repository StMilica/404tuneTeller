from tests.conftest import create_stock, create_prices

def test_profit_endpoint(client, app):
    stock_id = create_stock(app, symbol="TST", founded="2020-01-01")
    create_prices(app, stock_id, start_price=100, step=1, days=10, start_date="2020-01-01")

    response = client.get("/api/stocks/TST/profit?start=2020-01-01&end=2020-01-05")
    assert response.status_code == 200
    data = response.get_json()
    assert "main_range" in data
    assert data["main_range"]["best_trade"]["profit"] > 0
    assert data["stock"] == "TST"

def test_get_prices_from_db(client, app):
    stock_id = create_stock(app, symbol="TST", founded="2020-01-01")
    create_prices(app, stock_id, start_price=150, days=1, start_date="2020-01-02")

    response = client.get("/api/db/stocks/TST/prices")
    assert response.status_code == 200
    data = response.get_json()
    assert data["stock"] == "TST"
    assert len(data["prices"]) == 1
    assert data["prices"][0]["close"] == 150.0

def test_profit_route_valid(client, app):
    stock_id = create_stock(app, symbol="TST", founded="2022-01-01")
    create_prices(app, stock_id, start_price=100, step=1, days=10)

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

def test_better_stock_profit(client, app):
    s1_id = create_stock(app, "AAA", founded="2022-01-01")
    s2_id = create_stock(app, "BBB", founded="2022-01-01")
    create_prices(app, s1_id, start_price=100, step=1, days=10)
    create_prices(app, s2_id, start_price=200, step=3, days=10)

    response = client.get("/api/stocks/AAA/profit?start=2022-01-01&end=2022-01-05")
    assert response.status_code == 200
    data = response.get_json()
    better = data.get("better_stocks", [])
    assert isinstance(better, list)
    assert any(stock["symbol"] == "BBB" for stock in better)
    assert data["stock"] == "AAA"

def test_no_better_stocks(client, app):
    x_id = create_stock(app, "X", founded="2022-01-01")
    y_id = create_stock(app, "Y", founded="2022-01-01")
    z_id = create_stock(app, "Z", founded="2022-01-01")
    create_prices(app, x_id, start_price=50, step=2)
    create_prices(app, y_id, start_price=50, step=2)
    create_prices(app, z_id, start_price=40, step=1)

    response = client.get("/api/stocks/X/profit?start=2022-01-01&end=2022-01-05")
    assert response.status_code == 200
    data = response.get_json()
    better = data.get("better_stocks", [])
    assert isinstance(better, list)
    assert len(better) == 0