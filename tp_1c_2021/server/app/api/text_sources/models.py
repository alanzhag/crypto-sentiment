from dataclasses import dataclass
from typing import List

from app import db


class TextSource(db.Model):
    name = db.Column(db.String, primary_key=True)
    enabled = db.Column(db.Boolean, nullable=False)


@dataclass
class TextSourceStatus:
    name: str
    enabled: bool


@dataclass
class TextSourcesStatusResponse:
    sources: List[TextSourceStatus]
