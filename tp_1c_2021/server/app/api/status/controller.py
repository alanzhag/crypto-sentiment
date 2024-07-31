from flask_restx import Resource

from app.api.auth.models import RoleName
from app.api.schemas import detailed_status_schema, simple_status_schema
from app.api.status.models import ApplicationStatus
from app.api.status.service.status_provider import StatusProvider
from app.http_auth import auth


class DetailedStatus(Resource):
    @auth.login_required(role=RoleName.ADMIN.name)
    def get(self):
        app_status = ApplicationStatus(services=StatusProvider.services_status())
        return detailed_status_schema.dump(app_status), 200


class SimpleStatus(Resource):
    def get(self):
        app_status = ApplicationStatus(services=StatusProvider.services_status())
        return simple_status_schema.dump(app_status), 200
