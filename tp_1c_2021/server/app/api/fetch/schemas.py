from marshmallow import fields
from marshmallow_enum import EnumField

from app.api.fetch.models import FetchJobStatus
from app.ext import ma


class FetchJobSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    status = EnumField(FetchJobStatus)
    created = fields.DateTime()
    started = fields.DateTime()
    ended = fields.DateTime()
    metrics = fields.Method("get_metrics")
    message = fields.String()
    results = fields.Integer()

    def get_metrics(self, obj):
        return {
            "duration": obj.duration
        }
