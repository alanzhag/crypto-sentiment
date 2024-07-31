from marshmallow import fields
from marshmallow_enum import EnumField

from app.api.status.models import ServiceState
from app.ext import ma


class ServiceStatusSchema(ma.Schema):
    name = fields.String()
    status = EnumField(ServiceState)
    message = fields.String()


class DetailedStatusSchema(ma.Schema):
    status = EnumField(ServiceState)
    detailed_message = fields.String(attribute='message')
    services = fields.Nested(ServiceStatusSchema, many=True)


class SimpleStatusSchema(ma.Schema):
    status = EnumField(ServiceState)
    message = fields.String()
