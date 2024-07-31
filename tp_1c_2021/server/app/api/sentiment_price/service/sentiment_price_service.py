import itertools
import uuid
from datetime import datetime
from typing import List

from app.api.nlp.models import SentimentPriceSnapshot
from app.api.sentiment_price.models import SentimentPriceSource
from app.api.sentiment_price.service.sentiment_resolver.strategies.mayority_or_random_sentiment_resolver import \
    MayorityOrRandomSentimentResolver


class SentimentPriceService:

    def __init__(self):
        self.sentiment_resolver = MayorityOrRandomSentimentResolver()

    def __group_by_symbol(self, sen_price_sour_list: List[SentimentPriceSource]) -> List[List[SentimentPriceSource]]:
        sorted_sen_price_sour_list = sorted(sen_price_sour_list, key=lambda i: i.symbol)
        groups = []
        for _, group in itertools.groupby(sorted_sen_price_sour_list, lambda i: i.symbol):
            groups.append(list(group))
        return groups

    def generate_sentiment_price_snapshot(self, sentiment_price_source_list: List[SentimentPriceSource]):
        grouped_by_symbol = self.__group_by_symbol(sentiment_price_source_list)
        sentiment_prices = [self.sentiment_resolver.resolve_sentiment(x) for x in grouped_by_symbol]
        return SentimentPriceSnapshot(
            sentiment_prices=sentiment_prices,
            timestamp=datetime.now(),
            id=str(uuid.uuid4())
        )


sentiment_price_service = SentimentPriceService()
