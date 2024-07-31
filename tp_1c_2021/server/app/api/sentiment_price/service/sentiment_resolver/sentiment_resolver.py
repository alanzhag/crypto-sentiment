import random
from typing import List, Dict

from flask_restx import abort

from app.api.sentiment_price.models import SentimentPriceSource, SentimentPrice
from app.api.text_analysis.models import Sentiment


class BaseSentimentResolver:

    def __init__(self):
        pass

    @staticmethod
    def validate_integrity(sentiment_price_source_list: List[SentimentPriceSource]):
        presumed_symbol = sentiment_price_source_list[0].symbol
        all_symbols = [sp.symbol for sp in sentiment_price_source_list]
        all_have_same_symbol = all([symbol == presumed_symbol for symbol in all_symbols])
        if not all_have_same_symbol:
            raise abort(400, f"SentimentPriceSource integrity validation -> Symbols are not the same: {all_symbols}")

        presumed_price = sentiment_price_source_list[0].price
        all_prices = [sp.price for sp in sentiment_price_source_list]
        all_have_same_price = all([price == presumed_price for price in all_prices])
        if not all_have_same_price:
            raise abort(400, f"SentimentPriceSource integrity validation -> Prices are not the same: {all_prices}")

    def select_winner(self, sentiment_count) -> Sentiment:
        max_count = max([count for count in sentiment_count.values()])

        sentiments_with_max_count = [sentiment for (sentiment, count) in sentiment_count.items() if count == max_count]

        if len(sentiments_with_max_count) == 1:
            computed_sentiment = sentiments_with_max_count[0]
        else:
            computed_sentiment = random.choice(sentiments_with_max_count)

        return computed_sentiment

    def apply_strategy(self, sentiment_price_source_list: List[SentimentPriceSource]) -> Dict[Sentiment, int]:
        pass

    def resolve_sentiment(self, sentiment_price_source_list: List[SentimentPriceSource]) -> SentimentPrice:
        self.validate_integrity(sentiment_price_source_list)
        sentiment_count = self.apply_strategy(sentiment_price_source_list)
        sentiment = self.select_winner(sentiment_count=sentiment_count)
        symbol = sentiment_price_source_list[0].symbol
        price = sentiment_price_source_list[0].price
        return SentimentPrice(symbol=symbol, sentiment=sentiment, price=price)
