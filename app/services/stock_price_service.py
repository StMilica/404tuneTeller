import os
import pandas as pd
from app.models.stock_price import StockPrice

class StockPriceService:
    def __init__(self):
        self.prices_by_symbol = {}

    def load_csv_for_symbol(self, symbol, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found.")

        df = pd.read_csv(filepath)
        if 'Date' not in df.columns or 'Close' not in df.columns:
            raise ValueError("CSV file must contain 'Date' and 'Close' columns.")

        prices = [
            StockPrice(row['Date'], row['Close'])
            for _, row in df.iterrows()
        ]

        # sort by date
        prices.sort(key=lambda x: x.date)

        self.prices_by_symbol[symbol.upper()] = prices
        return len(prices)  # number of prices loaded

    def get_prices(self, symbol):
        return self.prices_by_symbol.get(symbol.upper(), [])