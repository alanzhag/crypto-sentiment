from marshmallow import fields, post_load
from marshmallow_enum import EnumField

from app.api.sentiment_price.models import SentimentPriceSource
from app.api.text_analysis.models import Sentiment
from app.ext import ma


class SentimentPriceSourceSchema(ma.Schema):
    source = fields.String()
    symbol = fields.String()
    sentiment = EnumField(Sentiment)
    price = fields.Float()

    @post_load()
    def make_sentiment_price_source(self, data, **kwargs):
        return SentimentPriceSource(**data)


class SentimentPriceSchema(ma.Schema):
    symbol = fields.String()
    sentiment = EnumField(Sentiment)
    price = fields.Float()


class SentimentPriceSnapshotSchema(ma.Schema):
    sentiment_prices = fields.List(fields.Nested(SentimentPriceSchema))
    timestamp = fields.DateTime()
    id = fields.String()


class ComputedSentimentPriceSchema(ma.Schema):
    sentiment_prices = fields.List(fields.Nested(SentimentPriceSchema))
    timestamp = fields.DateTime()
