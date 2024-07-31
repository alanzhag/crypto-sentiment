from datetime import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class Text:
    id: str
    external_id: str
    content: str
    topic: str
    source: str
    timestamp: datetime
    retrieve_time: datetime
    link: str
    metadata: dict
    # batch_id: int


@dataclass
class TextsByTopic:
    topic: str
    texts: List[Text]
    status: dict


@dataclass
class GroupedSourceFetch:
    source_name: str
    by_topics: List[TextsByTopic]
    status: dict


@dataclass
class TextFetchResponse:
    results: List[GroupedSourceFetch]
    status: dict
