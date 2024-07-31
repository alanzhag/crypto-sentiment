from flask_restx import Resource

from .models import FetchJob
from .services.fetch_job_dispatcher_service import fetch_job_dispatcher_service
from ..auth.models import RoleName
from ..schemas import fetch_job_schema
from ...http_auth import auth


class FetchJobResource(Resource):
    @auth.login_required(role=RoleName.ADMIN.name)
    def get(self, job_id):
        fetch_job = FetchJob.query.get(job_id)
        if fetch_job:
            return fetch_job_schema.dump(fetch_job), 200
        else:
            return {"message": "Fetch job not found"}, 404


class FetchJobPetitionResource(Resource):
    @auth.login_required(role=RoleName.ADMIN.name)
    def post(self):
        fetch_job = fetch_job_dispatcher_service.dispatch_fetch_job()
        return fetch_job_schema.dump(fetch_job), 200
