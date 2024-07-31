from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.api.crypto_price.models import CryptoPriceResponse
from app.api.sentiment_price.models import SentimentPriceSnapshot
from app.api.text_analysis.models import TextAnalysis


@dataclass
class TextRetrieveProperties:
    source: str
    topic: str
    id: str
    external_id: str
    link: str
    timestamp: datetime


@dataclass
class NLPTaggedText:
    text_retrieve_properties: TextRetrieveProperties
    text_analysis: TextAnalysis
    crypto_price: CryptoPriceResponse
    timestamp: datetime


@dataclass
class NLPTaggerResponse:
    results: List[NLPTaggedText]
    sentiment_price_snapshot: SentimentPriceSnapshot
    status: dict
