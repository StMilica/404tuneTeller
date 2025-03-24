from app.models.stock import Stock

class StockService:
    def __init__(self):
        self.stocks = []
        self.next_id = 1

    def list_stocks(self):
        return [stock.to_dict() for stock in self.stocks]
    
    def get_stock(self, stock_id):
        for stock in self.stocks:
            if stock.id == stock_id:
                return stock
        return None
    
    def create_stock(self, stock_data):
        stock = Stock(
            name=stock_data.get('name'),
            symbol=stock_data.get('symbol'),
            founded=stock_data.get('founded'),
            description=stock_data.get('description')
        )
        stock.id = self.next_id
        self.next_id += 1
        self.stocks.append(stock)
        return stock
    
    def update_stock(self, stock_id, data):
        stock = self.get_stock(stock_id)
        if not stock:
            return None
        
        stock.name = data.get('name', stock.name)
        stock.symbol = data.get('symbol', stock.symbol)
        stock.founded = data.get('founded', stock.founded)
        stock.description = data.get('description', stock.description)

        return stock
    
    def delete_stock(self, stock_id):
        stock = self.get_stock(stock_id)
        if stock:
            self.stocks.remove(stock)
            return True
        return False