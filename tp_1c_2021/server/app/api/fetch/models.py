import enum
import logging
from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from app import db


class FetchJobStatus(enum.Enum):
    WAITING = 1,
    RUNNING = 2,
    FINISHED = 3,
    ERROR = 4


class FetchJob(db.Model):
    id = db.Column('job_id', db.Integer, primary_key=True)
    status = db.Column(db.Enum(FetchJobStatus), default=FetchJobStatus.WAITING)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    started = db.Column(db.DateTime)
    ended = db.Column(db.DateTime)
    message = db.Column(db.String)
    results = db.Column(db.Integer, default=0)

    @hybrid_property
    def duration(self):
        if self.started and self.ended:
            return (self.ended - self.started).total_seconds()
        else:
            return 0

    def mark_as_started(self):
        self.started = datetime.now()
        self.status = FetchJobStatus.RUNNING
        db.session.commit()
        logging.info(f"FetchJob {self.id} marked as started")

    def mark_as_finished(self, results):
        self.ended = datetime.now()
        self.status = FetchJobStatus.FINISHED
        self.results = results
        db.session.commit()
        logging.info(f"FetchJob {self.id} marked as finished. {results} texts processed.")

    def mark_as_failed(self, e):
        self.ended = datetime.now()
        self.status = FetchJobStatus.ERROR
        self.message = str(e)
        db.session.commit()
        logging.info(f"FetchJob {self.id} marked as failed. Reason: {str(e)}")
