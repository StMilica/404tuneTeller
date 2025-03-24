from app import db
from datetime import datetime

class StockPrice(db.Model):
    __tablename__ = 'stock_prices'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    close = db.Column(db.Float, nullable=False)

    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)

    def __repr__(self):
        return f'<StockPrice {self.date} = {self.close}>'