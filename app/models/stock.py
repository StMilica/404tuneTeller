from datetime import datetime, date
from app import db

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    founded = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)

    # One-to-many relationship with StockPrice
    prices = db.relationship('StockPrice', backref='stock', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Stock {self.symbol}>'
 