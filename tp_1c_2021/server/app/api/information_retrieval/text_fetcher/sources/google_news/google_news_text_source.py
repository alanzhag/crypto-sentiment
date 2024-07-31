import logging
import uuid
from datetime import datetime, timezone, timedelta

from GoogleNews import GoogleNews
from newspaper import Article

from app.api.information_retrieval.models import Text
from app.api.information_retrieval.text_fetcher.commons.utils import article_config
from app.api.information_retrieval.text_fetcher.sources.base_text_source import BaseTextSource

"""
Source:
https://pypi.org/project/GoogleNews/
https://searchengineland.com/searching-google-in-past-minutes-or-seconds-25764
https://newspaper.readthedocs.io/en/latest/
https://medium.com/analytics-vidhya/googlenews-api-live-news-from-google-news-using-python-b50272f0a8f0
"""


def parse_minutes_ago(expression: str) -> int:
    number, unit, ago = expression.lower().split(" ")
    if "mins" in unit:
        return int(number)
    else:
        logging.error(f"Unexpected expression {expression}")
        return 0


class GoogleNewsTextSource(BaseTextSource):

    def __init__(self):
        super().__init__(name="google_news")
        self.google_news = GoogleNews(period="n60", lang="en")  # Last 60 minutes
        self.article_config = article_config()

    def search(self, query: str, n: int = 1):
        self.google_news.search(query)
        results = self.google_news.result()
        logging.debug(f"GoogleNews search for {query} threw {len(results)} results")
        return self.google_news.result()[:n]

    def map_to_text(self, search_result, topic) -> Text:
        logging.debug(f"Article parsing in process for {search_result['link']}")
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        article = Article(search_result['link'], config=self.article_config)
        article.download()
        article.parse()
        article.nlp()
        timestamp = article.publish_date.replace(tzinfo=timezone.utc) if article.publish_date \
            else now - timedelta(minutes=parse_minutes_ago(search_result["date"]))
        time_ago = now - timestamp
        _id = str(uuid.uuid4())
        return Text(
            id=_id,
            external_id=_id,
            content=article.text,
            topic=topic,
            source=self.name,
            timestamp=timestamp,
            retrieve_time=now,
            link=search_result["link"],
            metadata={"time_ago": str(time_ago), "has_pubdate": article.publish_date is not None}
        )
