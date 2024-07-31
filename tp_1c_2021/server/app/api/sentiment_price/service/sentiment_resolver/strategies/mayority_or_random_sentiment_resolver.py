from typing import List, Dict

from app.api.sentiment_price.models import SentimentPriceSource
from app.api.sentiment_price.service.sentiment_resolver.sentiment_resolver import BaseSentimentResolver
from app.api.text_analysis.models import Sentiment


class MayorityOrRandomSentimentResolver(BaseSentimentResolver):

    def __init__(self):
        super().__init__()

    def apply_strategy(self, sentiment_price_source_list: List[SentimentPriceSource]) -> Dict[Sentiment, int]:
        sentiment_list = [sp.sentiment for sp in sentiment_price_source_list]
        return {sentiment: sentiment_list.count(sentiment) for sentiment in Sentiment.list()}
