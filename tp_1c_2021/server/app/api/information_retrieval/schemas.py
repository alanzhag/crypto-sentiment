from marshmallow import fields

from app.ext import ma


class TextSchema(ma.Schema):
    id = fields.String()
    external_id = fields.String()
    content = fields.String()
    topic = fields.String()
    source = fields.String()
    timestamp = fields.DateTime()
    retrieve_time = fields.DateTime()
    link = fields.String()
    metadata = fields.Dict()


class TextsByTopicSchema(ma.Schema):
    topic = fields.String()
    texts = fields.Nested(TextSchema, many=True)
    status = fields.Dict()


class GroupedSourceFetchSchema(ma.Schema):
    source_name = fields.String()
    by_topics = fields.Nested(TextsByTopicSchema, many=True)
    status = fields.Dict()


class TextFetchResponseSchema(ma.Schema):
    results = fields.Nested(GroupedSourceFetchSchema, many=True)
    status = fields.Dict()
