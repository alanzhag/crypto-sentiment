import logging
from timeit import default_timer as timer
from typing import List

from app.api.crypto_price.services.crypto_price_service import CryptoPriceService, crypto_price_service
from app.api.information_retrieval.text_fetcher.text_fetcher import text_fetcher, TextFetcher
from app.api.nlp.models import NLPTaggedText, NLPTaggerResponse, TextRetrieveProperties, SentimentPriceSnapshot
from app.api.sentiment_price.models import SentimentPriceSource
from app.api.sentiment_price.service.sentiment_price_service import SentimentPriceService, sentiment_price_service
from app.api.text_analysis.services.text_analyser import text_analyser, TextAnalyser
from app.commons.utils import ArgDefaultDict


class NLPTaggerService:

    def __init__(self):
        self.text_analyser: TextAnalyser = text_analyser
        self.text_fetcher: TextFetcher = text_fetcher
        self.crypto_pricer: CryptoPriceService = crypto_price_service
        self.sentiment_price_service: SentimentPriceService = sentiment_price_service

    def __generate_sentiment_price_snapshot(self, texts: List[NLPTaggedText]) -> SentimentPriceSnapshot:
        sentiment_price_source_list = [
            SentimentPriceSource(
                symbol=text.crypto_price.symbol,
                sentiment=text.text_analysis.sentiment,
                price=text.crypto_price.price,
                source=text.text_retrieve_properties.source
            )
            for text in texts
        ]
        return self.sentiment_price_service.generate_sentiment_price_snapshot(sentiment_price_source_list)

    def fetch_and_tag(self, source: str = None, qty: int = 1) -> NLPTaggerResponse:
        logging.info("Proceeding to fetch texts and tag them with nlp features")
        time_start = timer()
        text_fetch_response = self.text_fetcher.fetch(source=source, n=qty)
        results = []
        price_cache = ArgDefaultDict(lambda symbol: self.crypto_pricer.get_price(symbol))
        for result in text_fetch_response.results:
            for text_by_topic in result.by_topics:
                for text in text_by_topic.texts:
                    text_properties = TextRetrieveProperties(
                        source=text.source,
                        topic=text.topic,
                        id=text.id,
                        external_id=text.external_id,
                        link=text.link,
                        timestamp=text.timestamp
                    )
                    text_analysis = self.text_analyser.analyse(text.content)
                    results.append(
                        NLPTaggedText(
                            text_retrieve_properties=text_properties,
                            text_analysis=text_analysis,
                            crypto_price=price_cache[text.topic],
                            timestamp=text.timestamp
                        )
                    )
        snapshot = self.__generate_sentiment_price_snapshot(results)
        time_took = timer() - time_start
        logging.info("NLP tagging done!")
        return NLPTaggerResponse(results=results, sentiment_price_snapshot=snapshot, status={"elapsed_time": time_took})


nlp_tagger_service = NLPTaggerService()
