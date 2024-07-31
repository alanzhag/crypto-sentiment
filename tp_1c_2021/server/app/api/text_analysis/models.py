import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Tuple, List


class Sentiment(enum.Enum):
    NEGATIVE = 0
    NEUTRAL = 1
    POSITIVE = 2

    @staticmethod
    def list():
        return [e for e in Sentiment]


@dataclass
class TextAnalysis:
    original_text: str
    sanitized_text: str
    processed_text: str
    sentiment: Sentiment
    polarity: float
    subjectivity: float
    frequency: Dict[str, List[str]]
    ner: List[Tuple[str, str]]
    timestamp: datetime = datetime.now()
