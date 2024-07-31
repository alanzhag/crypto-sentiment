from marshmallow import fields

from app.ext import ma


class TextSource(ma.Schema):
    name = fields.String()
    enabled = fields.Boolean()


class TextSourcesSchema(ma.Schema):
    sources = fields.List(fields.Nested(TextSource))
