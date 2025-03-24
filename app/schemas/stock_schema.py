from marshmallow import Schema, fields, validate

class StockSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    symbol = fields.Str(required=True, validate=validate.Length(equal=4))
    founded = fields.Date(required=True, format='%Y-%m-%d')
    description = fields.Str()