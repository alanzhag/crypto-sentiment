from marshmallow import fields

from app.ext import ma


class ExceptionMessageSchema(ma.Schema):
    status = fields.Integer()
    message = fields.String()


exception_message_schema = ExceptionMessageSchema()
