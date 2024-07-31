import logging
import uuid
import requests
from datetime import datetime, timezone
from typing import List
from newspaper import Article
from timeit import default_timer as timer

from app.api.information_retrieval.models import Text
from app.api.information_retrieval.text_fetcher.commons.utils import article_config, add_elapsed_time
from app.api.information_retrieval.text_fetcher.sources.base_text_source import BaseTextSource
from config import Config


class NewsTextSource(BaseTextSource):

    def __init__(self):
        super().__init__(name="news")
        self.api_key = Config.NEWS_API_KEY
        self.article_config = article_config()

    def search(self, query: str, n: int = 1):
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&pageSize={n}&apiKey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        news = response.json()["articles"]
        logging.debug(f"News.org search for {query} threw {len(news)} results")
        return news[:n]

    def map_to_text(self, search_result, topic):
        logging.debug(f"Article parsing in process for {search_result['url']}")
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        timestamp = datetime.strptime(search_result["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        time_ago = now - timestamp
        article = Article(search_result['url'], config=self.article_config)
        article.download()
        article.parse()
        article.nlp()
        _id = str(uuid.uuid4())
        return Text(
            id=_id,
            external_id=_id,
            content=article.text,
            topic=topic,
            source=self.name,
            timestamp=timestamp,
            retrieve_time=datetime.now(),
            link=search_result["url"],
            metadata={"time_ago": str(time_ago), "real_source": search_result["source"]["name"]}
        )