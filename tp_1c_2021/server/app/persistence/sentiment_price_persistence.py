from typing import List

from app.api.schemas import sentiment_price_snapshot_schema
from app.api.sentiment_price.models import SentimentPrice
from app.persistence.services.firebase_persistence import firebase_persistence_service


class SentimentPricePersistence:

    def __init__(self):
        self.collection = u"sentiment_price_snapshot"
        self.persistence_service = firebase_persistence_service

    def persist_snapshot(self, snapshot):
        data = sentiment_price_snapshot_schema.dump(snapshot)
        self.persistence_service.persist(self.collection, data)

    def get_last_n_snapshots(self, n: int = 1) -> List[SentimentPrice]:
        data = self.persistence_service.get_last_n(collection=self.collection, n=n)
        return sentiment_price_snapshot_schema.load(data, many=True)

    def get_snapshot(self, snapshot_id) -> SentimentPrice:
        data = self.persistence_service.get(self.collection, u"id", _id=snapshot_id)
        return sentiment_price_snapshot_schema.load(data)


sentiment_price_persistence_service = SentimentPricePersistence()
