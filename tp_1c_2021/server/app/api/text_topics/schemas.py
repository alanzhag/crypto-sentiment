from marshmallow import fields

from app.ext import ma


class TextTopicsSchema(ma.Schema):
    topics = fields.List(fields.String())
