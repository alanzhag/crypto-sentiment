import logging
from typing import List

from app.api.information_retrieval.models import Text
from timeit import default_timer as timer

from app.api.information_retrieval.text_fetcher.commons.utils import add_elapsed_time


class BaseTextSource:

    def __init__(self, name):
        self.name = name

    def search(self, query: str, n: int = 1):
        return []

    def map_to_text(self, search_result, topic) -> Text:
        pass

    def fetch(self, topic: str, n: int = 1) -> List[Text]:
        texts = []
        for search_result in self.search(topic, n):
            try:
                mapping_start = timer()
                text = self.map_to_text(search_result, topic)
                add_elapsed_time(text, elapsed_time=timer() - mapping_start)
                texts.append(text)
            except RuntimeError as e:
                logging.error(f"Processing of {search_result['url']} in source {self.name} failed. Reason: {str(e)}")
                continue
        return texts
