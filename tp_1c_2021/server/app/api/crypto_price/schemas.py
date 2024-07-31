from marshmallow import fields

from app.ext import ma


class CryptoPriceSchema(ma.Schema):
    symbol = fields.String()
    currency = fields.String()
    price = fields.Float()
    last_update = fields.DateTime()
    error = fields.Boolean()
