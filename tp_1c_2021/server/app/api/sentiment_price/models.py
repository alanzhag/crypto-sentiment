from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.api.text_analysis.models import Sentiment


@dataclass
class SentimentPrice:
    symbol: str
    sentiment: Sentiment
    price: float


@dataclass
class SentimentPriceSource:
    source: str
    symbol: str
    sentiment: Sentiment
    price: float


@dataclass
class SentimentPriceSnapshot:
    sentiment_prices: List[SentimentPrice]
    timestamp: datetime
    id: str
