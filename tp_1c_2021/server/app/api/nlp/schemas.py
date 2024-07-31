from marshmallow import fields
from marshmallow_enum import EnumField

from app.api.crypto_price.schemas import CryptoPriceSchema
from app.api.sentiment_price.schemas import SentimentPriceSnapshotSchema
from app.api.text_analysis.models import Sentiment
from app.ext import ma


class TextRetrievePropertiesSchema(ma.Schema):
    source = fields.String()
    topic = fields.String()
    id = fields.String()
    external_id = fields.String()
    link = fields.String()
    timestamp = fields.DateTime()


class ShortTextAnalysisSchema(ma.Schema):
    original_text = fields.String()
    processed_text = fields.String()
    sentiment = EnumField(Sentiment)
    frequency = fields.Dict()
    ner = fields.Dict()
    timestamp = fields.DateTime()


class ShortCryptoPriceSchema(ma.Schema):
    symbol = fields.String()
    currency = fields.String()
    price = fields.Float()


class NLPTaggedTextSchema(ma.Schema):
    text_retrieve_properties = fields.Nested(TextRetrievePropertiesSchema)
    text_analysis = fields.Nested(ShortTextAnalysisSchema)
    crypto_price = fields.Nested(CryptoPriceSchema)
    timestamp = fields.DateTime()


class NLPTaggerResponseSchema(ma.Schema):
    results = fields.Nested(NLPTaggedTextSchema, many=True)
    sentiment_price_snapshot = fields.Nested(SentimentPriceSnapshotSchema)
    status = fields.Dict()
