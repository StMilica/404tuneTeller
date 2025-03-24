from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
from app.models.stock import Stock
from app import db

class StockSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Stock
        load_instance = True  # allows .load() to return Stock objects
        sqla_session = db.session
        include_relationships = False
        include_fk = False

    # Override default field settings for custom validation
    name = fields.Str(required=True, validate=validate.Length(min=1))
    symbol = fields.Str(required=True, validate=validate.Length(min=1, max=10))
    founded = fields.Date(required=True, format='%Y-%m-%d')
    description = fields.Str()