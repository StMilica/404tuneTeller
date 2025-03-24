from app import db
from app.models.stock import Stock

class StockService:

    def list_stocks(self):
        return Stock.query.all()

    def get_stock(self, stock_id):
        return Stock.query.get(stock_id)

    def create_stock(self, stock):
        db.session.add(stock)
        db.session.commit()
        return stock

    def update_stock(self, stock_id, data):
        stock = self.get_stock(stock_id)
        if not stock:
            return None

        stock.name = data.get("name", stock.name)
        stock.symbol = data.get("symbol", stock.symbol)
        stock.founded = data.get("founded", stock.founded)
        stock.description = data.get("description", stock.description)

        db.session.commit()
        return stock

    def delete_stock(self, stock_id):
        stock = self.get_stock(stock_id)
        if not stock:
            return False

        db.session.delete(stock)
        db.session.commit()
        return True