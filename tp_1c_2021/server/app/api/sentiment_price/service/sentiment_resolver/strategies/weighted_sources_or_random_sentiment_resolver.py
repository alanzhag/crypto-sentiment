from collections import defaultdict
from typing import List, Dict

from app.api.sentiment_price.models import SentimentPriceSource
from app.api.sentiment_price.service.sentiment_resolver.sentiment_resolver import BaseSentimentResolver
from app.api.text_analysis.models import Sentiment


class WeightedSourcesOrRandomSentimentResolver(BaseSentimentResolver):

    def __init__(self):
        super().__init__()
        self.source_weights = defaultdict(lambda: 1, {
            "twitter": 3,
            "reddit": 2,
            "news": 1,
            "google_news": 1
        })

    def apply_strategy(self, sentiment_price_source_list: List[SentimentPriceSource]) -> Dict[Sentiment, int]:
        sentiment_count = {}

        for sp in sentiment_price_source_list:
            sentiment_source_weight = self.source_weights[sp.source]
            if sp.sentiment in sentiment_count.keys():
                sentiment_count[sp.sentiment] = sentiment_count[sp.sentiment] + sentiment_source_weight
            else:
                sentiment_count[sp.sentiment] = sentiment_source_weight

        return sentiment_count
