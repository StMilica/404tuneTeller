from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.stock_service import StockService
from app.schemas.stock_schema import StockSchema

stock_routes = Blueprint('stock_routes', __name__)
stock_service = StockService()

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