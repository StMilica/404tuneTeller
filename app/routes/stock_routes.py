from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from marshmallow import ValidationError

from app.services.stock_service import StockService
from app.services.stock_price_service import StockPriceService
from app.services.profit_calculator import ProfitCalculatorService
from app.schemas.stock_schema import StockSchema
from app.models.stock import Stock
from app.models.stock_price import StockPrice

stock_routes = Blueprint('stock_routes', __name__)
stock_service = StockService()
stock_price_service = StockPriceService()

@stock_routes.route('/api/stocks', methods=['GET'])
def get_stocks():
    schema = StockSchema(many=True)
    return schema.dump(stock_service.list_stocks()), 200

@stock_routes.route('/api/stocks/<int:stock_id>', methods=['GET'])
def get_stock(stock_id):
    stock = stock_service.get_stock(stock_id)
    if stock:
        schema = StockSchema()
        return schema.dump(stock), 200
    return jsonify({'error': 'Stock not found'}), 404

@stock_routes.route('/api/stocks', methods=['POST'])
def create_stock():
    data = request.get_json()
    schema = StockSchema()
    try:
        validated_data = schema.load(data)
        stock = stock_service.create_stock(validated_data)
        return schema.dump(stock), 201
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
@stock_routes.route('/api/stocks/<int:stock_id>', methods=['PUT'])
def update_stock(stock_id):
    data = request.get_json()
    schema = StockSchema(partial=True)
    try:
        validated_data = schema.load(data)
        stock = stock_service.update_stock(stock_id, validated_data)
        if stock:
            return schema.dump(stock)
        return jsonify({'error': 'Stock not found'}), 404
    except ValidationError as err:                                                                                                                                      
        return jsonify({'error': err.messages}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    

@stock_routes.route('/api/stocks/<int:stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    success = stock_service.delete_stock(stock_id)
    if success:
        return '', 204
    return jsonify({'error': 'Stock not found'}), 404

@stock_routes.route('/api/db/stocks/<string:symbol>/prices', methods=['GET'])
def get_prices_from_db(symbol):
    stock = Stock.query.filter_by(symbol=symbol.upper()).first()

    if not stock:
        return jsonify({'error': f'Stock with symbol {symbol} not found.'}), 404

    prices = StockPrice.query.filter_by(stock_id=stock.id).order_by(StockPrice.date).all()
    data = [
        {'date': price.date.strftime('%Y-%m-%d'), 'close': price.close}
        for price in prices
    ]

    return jsonify({
        'stock': stock.symbol,
        'prices': data
    }), 200

@stock_routes.route('/api/stocks/<string:symbol>/profit', methods=['GET'])
def calculate_profit(symbol):
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    if not start_str or not end_str:
        return jsonify({'error': 'Query parameters "start" and "end" are required'}), 400

    try:
        start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if start_date > end_date:
        return jsonify({'error': '"start" must be before "end"'}), 400

    stock = Stock.query.filter_by(symbol=symbol.upper()).first()
    if not stock:
        return jsonify({'error': f'Stock {symbol} not found'}), 404

    period_days = (end_date - start_date).days + 1

    # Fetch 3 ranges: before, target, after
    prices = StockPrice.query.filter_by(stock_id=stock.id).order_by(StockPrice.date).all()

    def get_prices_in_range(start, end):
        return [p for p in prices if start <= p.date <= end]

    main_prices = get_prices_in_range(start_date, end_date)
    prev_prices = get_prices_in_range(start_date - timedelta(days=period_days), start_date - timedelta(days=1))
    next_prices = get_prices_in_range(end_date + timedelta(days=1), end_date + timedelta(days=period_days))

    # Optional: find stocks with better total profit in the same range
    better_stocks = []
    target_profit = ProfitCalculatorService.get_total_profit(main_prices)

    all_stocks = Stock.query.all()

    for other_stock in all_stocks:
        if other_stock.id == stock.id:
            continue  # skip the one we already calculated

        other_prices = StockPrice.query.filter_by(stock_id=other_stock.id).all()
        prices_in_range = [p for p in other_prices if start_date <= p.date <= end_date]

        other_profit = ProfitCalculatorService.get_total_profit(prices_in_range)

        if other_profit > target_profit:
            better_stocks.append({
                "symbol": other_stock.symbol,
                "total_profit": round(other_profit, 2)
            })


    return jsonify({
        "stock": stock.symbol,
        "main_range": {
            "start": start_str,
            "end": end_str,
            "best_trade": ProfitCalculatorService.get_best_trade(main_prices),
            "total_profit": ProfitCalculatorService.get_total_profit(main_prices)
        },
        "previous_range": {
            "start": (start_date - timedelta(days=period_days)).strftime('%Y-%m-%d'),
            "end": (start_date - timedelta(days=1)).strftime('%Y-%m-%d'),
            "best_trade": ProfitCalculatorService.get_best_trade(prev_prices),
            "total_profit": ProfitCalculatorService.get_total_profit(prev_prices)
        },
        "next_range": {
            "start": (end_date + timedelta(days=1)).strftime('%Y-%m-%d'),
            "end": (end_date + timedelta(days=period_days)).strftime('%Y-%m-%d'),
            "best_trade": ProfitCalculatorService.get_best_trade(next_prices),
            "total_profit": ProfitCalculatorService.get_total_profit(next_prices)
        },
        "better_stocks": better_stocks
    }), 200


# In-memory support for stock prices
# import os
# @stock_routes.route('/api/stocks/upload-prices', methods=['POST'])
# def upload_prices():
#     data = request.get_json()
#     symbol = data.get('symbol')
#     filename = data.get('filename')

#     if not symbol or not filename:
#         return jsonify({'error': 'Both symbol and filename are required.'}), 400

#     filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', filename))

#     try:
#         count = stock_price_service.load_csv_for_symbol(symbol, filepath)
#         return jsonify({'message': f'Loaded {count} prices for {symbol}.'}), 200
#     except FileNotFoundError:
#         return jsonify({'error': f'File {filename} not found.'}), 404
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 400
    
# @stock_routes.route('/api/stocks/<string:symbol>/prices', methods=['GET'])
# def get_stock_prices(symbol):
#     prices = stock_price_service.get_prices(symbol)

#     if not prices:
#         return jsonify({'error': f'No prices found for symbol {symbol}'}), 404

#     data = [price.to_dict() for price in prices]
#     return jsonify(data), 200