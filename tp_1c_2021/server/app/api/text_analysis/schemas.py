from marshmallow import fields
from marshmallow_enum import EnumField

from app.api.text_analysis.models import Sentiment
from app.ext import ma


class TextAnalysisSchema(ma.Schema):
    original_text = fields.String()
    sanitized_text = fields.String()
    processed_text = fields.String()
    sentiment = EnumField(Sentiment)
    polarity = fields.Float()
    subjectivity = fields.Float()
    polarity_scores = fields.Dict()
    frequency = fields.Dict()
    ner = fields.Dict()
    timestamp = fields.DateTime()
