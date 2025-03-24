from datetime import datetime, date

class Stock:
    def __init__(self, name, symbol, founded, description=None):
        self.id = None # This will be set by the database
        self.name = name
        self.symbol = symbol
        self.founded = self.parse_date(founded)
        self.description = description

    def parse_date(self, value):
        if isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d').date()
        elif isinstance(value, date):
            return value
        else:
            raise ValueError("Invalid date format for 'founded'")
 