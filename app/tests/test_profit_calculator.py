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

def test_always_increasing():
    prices = [
        create_price(date(2022, 1, 1), 10),
        create_price(date(2022, 1, 2), 12),
        create_price(date(2022, 1, 3), 14),
        create_price(date(2022, 1, 4), 16)
    ]

    best = ProfitCalculatorService.get_best_trade(prices)
    total = ProfitCalculatorService.get_total_profit(prices)

    assert best["buy_price"] == 10
    assert best["sell_price"] == 16
    assert best["profit"] == 6
    assert total == 6  # all upward moves summed

def test_always_decreasing():
    prices = [
        create_price(date(2022, 1, 1), 16),
        create_price(date(2022, 1, 2), 14),
        create_price(date(2022, 1, 3), 12),
        create_price(date(2022, 1, 4), 10)
    ]

    best = ProfitCalculatorService.get_best_trade(prices)
    total = ProfitCalculatorService.get_total_profit(prices)

    assert best["profit"] == 0
    assert best["buy_date"] is None
    assert total == 0

def test_single_vs_multiple_diff():
    prices = [
        create_price(date(2022, 1, 1), 10),
        create_price(date(2022, 1, 2), 12),
        create_price(date(2022, 1, 3), 11),
        create_price(date(2022, 1, 4), 14),
        create_price(date(2022, 1, 5), 13)
    ]

    best = ProfitCalculatorService.get_best_trade(prices)
    total = ProfitCalculatorService.get_total_profit(prices)

    assert best["buy_price"] == 10
    assert best["sell_price"] == 14
    assert best["profit"] == 4
    assert total == 5  # +2 (10→12) +3 (11→14)

def test_complex_fluctuations():
    prices = [
        create_price(date(2022, 1, 1), 15),
        create_price(date(2022, 1, 2), 10),
        create_price(date(2022, 1, 3), 20),
        create_price(date(2022, 1, 4), 18),
        create_price(date(2022, 1, 5), 25),
        create_price(date(2022, 1, 6), 5),
        create_price(date(2022, 1, 7), 30)
    ]

    best = ProfitCalculatorService.get_best_trade(prices)
    total = ProfitCalculatorService.get_total_profit(prices)

    assert best["buy_price"] == 5
    assert best["sell_price"] == 30
    assert best["profit"] == 25
    assert total == 42  # +10 (10→20) +7 (18→25) +25 (5→30) = 42 (minus one drop)

def test_empty_price_list():
    prices = []

    best = ProfitCalculatorService.get_best_trade(prices)
    total = ProfitCalculatorService.get_total_profit(prices)

    assert best is None
    assert total == 0.0

def test_single_price():
    prices = [create_price(date(2022, 1, 1), 100)]

    best = ProfitCalculatorService.get_best_trade(prices)
    total = ProfitCalculatorService.get_total_profit(prices)

    assert best["profit"] == 0
    assert best["buy_date"] is None
    assert total == 0.0