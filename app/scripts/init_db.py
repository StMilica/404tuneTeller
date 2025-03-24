import os
import pandas as pd
from datetime import datetime

from app import db, create_app
from app.models.stock import Stock
from app.models.stock_price import StockPrice

app = create_app()

def load_stock_with_prices(symbol, name, founded, description, filename):
    with app.app_context():
        # Add Stock
        stock = Stock.query.filter_by(symbol=symbol).first()
        if not stock:
            stock = Stock(
                name=name,
                symbol=symbol,
                founded=datetime.strptime(founded, "%Y-%m-%d").date(),
                description=description
            )
            db.session.add(stock)
            db.session.commit()
            print(f"Stock '{symbol}' added.")

        # Read CSV and add StockPrices
        path = os.path.abspath(os.path.join('app', 'data', filename))
        df = pd.read_csv(path)

        for _, row in df.iterrows():
            try:
                date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
                close = float(row['Close'])

                existing = StockPrice.query.filter_by(stock_id=stock.id, date=date).first()
                if not existing:
                    price = StockPrice(date=date, close=close, stock_id=stock.id)
                    db.session.add(price)
            except Exception as e:
                print(f"Error in row: {row} → {e}")

        db.session.commit()
        print(f"Prices for '{symbol}' are added ({len(df)} rows).")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_stock_with_prices(
            symbol="FB",
            name="Facebook Inc.",
            founded="2004-02-04",
            description="Social media and tech company",
            filename="Facebook.csv"
        )