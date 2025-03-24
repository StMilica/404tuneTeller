import pytest
from datetime import date
from app.models.stock_price import StockPrice
from app.services.profit_calculator import ProfitCalculatorService

def create_price(d, c):
    return StockPrice(date=d, close=c)

def test_best_trade_basic():
    prices = [
        create_price(date(2020, 1, 1), 100),
        create_price(date(2020, 1, 2), 80),
        create_price(date(2020, 1, 3), 120),  # <-- sell
        create_price(date(2020, 1, 4), 90),
    ]

    result = ProfitCalculatorService.get_best_trade(prices)
    assert result["buy_date"] == "2020-01-02"
    assert result["sell_date"] == "2020-01-03"
    assert result["profit"] == 40.0

def test_best_trade_no_profit():
    prices = [
        create_price(date(2020, 1, 1), 100),
        create_price(date(2020, 1, 2), 90),
        create_price(date(2020, 1, 3), 85),
    ]

    result = ProfitCalculatorService.get_best_trade(prices)
    assert result["profit"] == 0

def test_total_profit_basic():
    prices = [
        create_price(date(2020, 1, 1), 100),
        create_price(date(2020, 1, 2), 110),
        create_price(date(2020, 1, 3), 105),
        create_price(date(2020, 1, 4), 115),
    ]

    result = ProfitCalculatorService.get_total_profit(prices)
    assert result == 20.0  # +10 (100→110), +10 (105→115)