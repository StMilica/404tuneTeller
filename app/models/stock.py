from datetime import datetime, date
from app import db

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    founded = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Stock {self.symbol}>'
    
from app.models.stock_price import StockPrice
Stock.prices = db.relationship('StockPrice', backref='stock', lazy=True, cascade="all, delete-orphan")
 