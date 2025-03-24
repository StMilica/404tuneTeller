from app import create_app, db
from app.models.stock import Stock
from app.models.stock_price import StockPrice

import pandas as pd
from datetime import datetime
import os

app = create_app()

STOCKS = [
    {
        "symbol": "FB",
        "name": "Facebook Inc.",
        "founded": "2004-02-04",
        "filename": "Facebook.csv",
        "description": "Social media and tech company"
    },
    {
        "symbol": "GOOG",
        "name": "Google LLC",
        "founded": "1998-09-04",
        "filename": "Google.csv",
        "description": "Search and advertising platform"
    },
    {
        "symbol": "NFLX",
        "name": "Netflix Inc.",
        "founded": "1997-08-29",
        "filename": "Netflix.csv",
        "description": "Streaming and entertainment"
    },
    {
        "symbol": "AMZN",
        "name": "Amazon.com Inc.",
        "founded": "1994-07-05",
        "filename": "Amazon.csv",
        "description": "E-commerce and cloud computing"
    },
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "founded": "1976-04-01",
        "filename": "Apple.csv",
        "description": "Consumer electronics and software"
    }
]

def load_csv(filepath):
    df = pd.read_csv(filepath)
    df = df[["Date", "Close"]].dropna()
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df

def init_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        for stock_data in STOCKS:
            print(f"Loading: {stock_data['symbol']}")

            stock = Stock(
                name=stock_data["name"],
                symbol=stock_data["symbol"],
                founded=datetime.strptime(stock_data["founded"], "%Y-%m-%d").date(),
                description=stock_data["description"]
            )
            db.session.add(stock)
            db.session.commit()

            path = os.path.abspath(os.path.join("app", "data", stock_data["filename"]))
            df = load_csv(path)

            prices = [
                StockPrice(date=row["Date"], close=row["Close"], stock_id=stock.id)
                for _, row in df.iterrows()
            ]
            db.session.add_all(prices)
            db.session.commit()
            print(f"Loaded {len(prices)} prices for {stock.symbol}")

if __name__ == "__main__":
    init_database()