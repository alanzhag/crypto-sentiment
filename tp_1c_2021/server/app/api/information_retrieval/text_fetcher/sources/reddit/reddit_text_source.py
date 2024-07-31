import logging
import uuid
from datetime import datetime, timedelta

import praw

from app.api.information_retrieval.models import Text
from app.api.information_retrieval.text_fetcher.sources.base_text_source import BaseTextSource
from config import Config

"""
Source:
https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
"""


class RedditTextSource(BaseTextSource):
    def __init__(self):
        super().__init__(name="reddit")
        self.reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            user_agent="nlp-utn-frba")

    def search(self, query: str, n: int = 1):
        all = self.reddit.subreddit("all")
        posts = list(all.search(query, limit=n + 4, time_filter='hour'))
        logging.debug(f"Reddit search for {query} threw {len(posts)} results")
        posts = [p for p in posts if
                 datetime.utcnow() - datetime.utcfromtimestamp(p.created_utc) < timedelta(minutes=60)]
        return posts[:n]

    def map_to_text(self, search_result, topic) -> Text:
        now = datetime.utcnow()
        return Text(
            id=str(uuid.uuid4()),
            external_id=search_result.id,
            content=search_result.selftext if search_result.selftext else search_result.title,
            topic=topic,
            source=self.name,
            timestamp=datetime.utcfromtimestamp(search_result.created_utc),
            retrieve_time=now,
            link=f"https://reddit.com{search_result.permalink}",
            metadata={
                "time_ago": str(now - datetime.utcfromtimestamp(search_result.created_utc)),
                "post_hint": search_result.post_hint if hasattr(search_result, "post_hint") else "",
                "created_utc": search_result.created_utc,
                "has_selftext": search_result.selftext != ""
            }
        )
