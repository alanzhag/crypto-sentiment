import logging
from typing import List

from app.api.nlp.models import NLPTaggedText
from app.api.schemas import nlp_tagged_text_schema
from app.api.text_sources.services.text_sources_service import text_sources_service
from app.commons.utils import flatten
from app.persistence.services.firebase_persistence import firebase_persistence_service


class TextPersistence:

    def __init__(self):
        self.collection = u"texts"
        self.persistence_service = firebase_persistence_service
        self.text_sources_service = text_sources_service

    def persist_text(self, text):
        data = nlp_tagged_text_schema.dump(text)
        self.persistence_service.persist(self.collection, data)

    def persist_texts(self, texts: List[NLPTaggedText]):
        logging.info(f"About to persist {len(texts)} texts")
        data = nlp_tagged_text_schema.dump(texts, many=True)
        self.persistence_service.persist_list(self.collection, data)

    def get_text(self, text_id):
        data = self.persistence_service.get(self.collection, u"text_retrieve_properties.id", _id=text_id)
        return nlp_tagged_text_schema.load(data)

    def get_all_texts(self):
        data = self.persistence_service.get_all(self.collection)
        return nlp_tagged_text_schema.load(data, many=True)

    def get_last_texts(self, limit: int = 1, offset: int = 0):
        data = self.persistence_service.get_last_n(collection=self.collection, limit=limit, offset=offset)
        return nlp_tagged_text_schema.load(data, many=True)

    def get_last_texts_from_all_sources(self, limit: int = 1, offset: int = 0):
        data = []
        sources = self.text_sources_service.get_active_sources_names()
        source_where_clauses = [(u"text_retrieve_properties.source", u"==", source) for source in sources]
        for where_clause in source_where_clauses:
            results = self.persistence_service.get_last_n(
                collection=self.collection,
                where_clauses=[where_clause],
                n=limit,
                offset=offset
            )
            data.append(results)
        data = flatten(data)
        return nlp_tagged_text_schema.load(data, many=True)


text_persistence_service = TextPersistence()
