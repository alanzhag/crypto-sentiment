from flask_restx import Resource, Namespace

from app.api.schemas import text_sources_schema
from app.api.text_sources.services.text_sources_service import text_sources_service

text_sources_ns = Namespace("textSources", "Text sources to lookup")


@text_sources_ns.route("")
class TextSources(Resource):
    # @auth.login_required()
    def get(self):
        response = text_sources_service.get_sources_status()
        return text_sources_schema.dump(response), 200
