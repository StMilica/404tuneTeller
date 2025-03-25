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
- Dockerized for consistent deployment
- Tested with pytest

---

## Local Setup (without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/init_db.py
python app.py
```

---

## Docker Setup

1. Make sure Docker is installed and running
2. From the project root, build and run:

```bash
docker compose up --build
```

3. Visit the API at:  
[http://localhost:5000/api/ping](http://localhost:5000/api/ping)

To stop:

```bash
docker compose down
```

---

## Postman Collection

To easily test API endpoints:

- Import the Postman collection file:  
  `postman/404tuneTeller_postman_collection.json`

### Includes:
- Ping check (`/api/ping`)
- Stock CRUD (POST, GET, DELETE)
- Stock price listing
- Profit analysis

---

## Example Request

```http
GET /api/stocks/FB/profit?start=2012-05-22&end=2012-06-01
```

Returns best trade, total profit, and better-performing stocks.

---

## Testing

```bash
pytest --cov=app --cov-report=term
```
