import logging

from app import db
from app.api.fetch.models import FetchJob
from app.api.nlp.models import NLPTaggerResponse
from app.api.nlp.services.nlp_tagger_service import nlp_tagger_service
from app.ext import executor
from app.persistence.sentiment_price_persistence import sentiment_price_persistence_service
from app.persistence.text_persistence import text_persistence_service


class FetchJobDispatcherService:

    def __init__(self):
        self.nlp_tagger_service = nlp_tagger_service
        self.text_persistence_service = text_persistence_service
        self.sentiment_price_persistence_service = sentiment_price_persistence_service

    def __create_fetch_job(self) -> FetchJob:
        fetch_job = FetchJob()
        db.session.add(fetch_job)
        db.session.commit()
        return fetch_job

    def __do_job(self, fetch_id):
        logging.info(f"Executor started with job_id {fetch_id}")
        fetch_job: FetchJob = FetchJob.query.get(fetch_id)
        fetch_job.mark_as_started()
        try:
            service_response: NLPTaggerResponse = self.nlp_tagger_service.fetch_and_tag()
            self.text_persistence_service.persist_texts(service_response.results)
            self.sentiment_price_persistence_service.persist_snapshot(service_response.sentiment_price_snapshot)
            fetch_job.mark_as_finished(results=len(service_response.results))
            logging.info(f"Executor finished with job_id {fetch_id}")
        except Exception as e:
            fetch_job.mark_as_failed(e)
            logging.error(f"There was a problem running the job {fetch_id}")

    def dispatch_fetch_job(self) -> FetchJob:
        fetch_job = self.__create_fetch_job()
        executor.submit(self.__do_job, fetch_job.id)
        return fetch_job

    def synchronic_fetch_job(self) -> FetchJob:
        fetch_job = self.__create_fetch_job()
        self.__do_job(fetch_job.id)
        return fetch_job


fetch_job_dispatcher_service = FetchJobDispatcherService()
