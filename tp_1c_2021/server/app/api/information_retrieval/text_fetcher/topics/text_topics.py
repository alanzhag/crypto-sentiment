from typing import List

from app.api.information_retrieval.text_fetcher.topics.models import TextTopic


class TextTopicsRepo:

    def __init__(self):
        pass

    def topics_from_db(self) -> List[str]:
        return [row.topic for row in TextTopic.query.all()]

    def topics(self) -> List[str]:
        return self.topics_from_db()


text_topics_repo = TextTopicsRepo()
