# 404tuneTeller

404tuneTeller is a Flask API for storing stock data and calculating trading profits from historical prices.

## Features

- CRUD for stocks
- CSV import of stock prices
- Profit analysis:
  - Best buy/sell pair
  - Total profit over date range
  - Comparison with other stocks
- SQLite + SQLAlchemy
- Tested with pytest

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/init_db.py
python app.py
```

## Example Request

```http
GET /api/stocks/FB/profit?start=2022-01-01&end=2022-01-10
```

Returns best trade, total profit, and better-performing stocks.

## Testing

```bash
pytest --cov=app --cov-report=term
```