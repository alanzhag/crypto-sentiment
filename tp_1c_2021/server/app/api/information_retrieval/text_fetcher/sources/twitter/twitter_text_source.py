import logging
import uuid
from datetime import datetime, timedelta
from timeit import default_timer as timer
from typing import List

import tweepy

from app.api.information_retrieval.models import Text
from app.api.information_retrieval.text_fetcher.commons.utils import add_elapsed_time
from app.api.information_retrieval.text_fetcher.sources.base_text_source import BaseTextSource
from config import Config

"""
Source:
https://www.toptal.com/python/twitter-data-mining-using-python
Tweepy doc
"""


class TwitterTextSource(BaseTextSource):
    def __init__(self):
        super().__init__(name="twitter")
        auth = tweepy.OAuthHandler(Config.TWEETER_CONSUMER_KEY, Config.TWEETER_CONSUMER_SECRET)
        auth.set_access_token(Config.TWEETER_ACCESS_TOKEN, Config.TWEETER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def search(self, query: str, n: int = 1):
        language = "en"
        results = self.api.search(q=query, lang=language, count=n + 2, tweet_mode='extended')
        results = [r for r in results if datetime.utcnow() - r.created_at < timedelta(minutes=60)]
        for tweet in results:
            logging.debug(f"{tweet.user.screen_name} tweeted: {tweet.full_text}")
        return results[:n]

    def map_to_text(self, search_result, topic) -> Text:
        if hasattr(search_result, "retweeted_status"):
            tweet_id = search_result.retweeted_status.id_str
            content = search_result.retweeted_status.full_text
            is_rt = True
        else:
            tweet_id = search_result.id_str
            content = search_result.full_text
            is_rt = False
        now = datetime.utcnow()
        time_ago = now - search_result.created_at
        return Text(
            id=str(uuid.uuid4()),
            external_id=tweet_id,
            content=content,
            topic=topic,
            source=self.name,
            timestamp=search_result.created_at,
            retrieve_time=now,
            link=f"https://twitter.com/twitter/statuses/{tweet_id}",
            metadata={
                "time_ago": str(time_ago),
                "from_rt": is_rt,
                "original_id": search_result.id_str
            } if is_rt else {"time_ago": str(time_ago)}
        )
