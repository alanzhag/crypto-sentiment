import logging

import firebase_admin
from firebase_admin import credentials, firestore

from config import FirebaseConfig


class FirebasePersistenceService:

    def __init__(self):
        cred = credentials.Certificate(FirebaseConfig.CERT)
        firebase_admin.initialize_app(cred)
        self.firestore_db = firestore.client()

    def persist(self, collection, element):
        logging.debug(f"Persisting {element} in {collection}")
        self.firestore_db.collection(collection).add(element)
        logging.debug(f"Element persisted!")

    def persist_list(self, collection, _list):
        for item in _list:
            self.persist(collection, item)

    def get_all(self, collection):
        return [result.to_dict() for result in self.firestore_db.collection(collection).get()]

    def get_last_n(self, collection, where_clauses=None, n: int = 1, offset: int = 0):
        if where_clauses is None:
            where_clauses = []
        results = self.firestore_db.collection(collection)
        for (condition, operator, value) in where_clauses:
            results = results.where(condition, operator, value)
        results = results.order_by("timestamp", direction="DESCENDING").offset(offset).limit(n).get()
        return [result.to_dict() for result in results]

    def get(self, collection, where_clause_identifier, _id):
        results = self.firestore_db.collection(collection).where(where_clause_identifier, u"==", _id).get()
        return results[0].to_dict() if results else None


firebase_persistence_service = FirebasePersistenceService()
