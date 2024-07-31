from flask import Blueprint
from flask_restx import Api, Namespace

from app.api.auth.token_based.controller import auth_ns
from app.api.crypto_price.controller import crypto_price_ns
from app.api.fetch.controller import FetchJobPetitionResource, FetchJobResource
from app.api.information_retrieval.controller import information_retrieval_ns
from app.api.maintenance.endpoints.controller import Endpoints
from app.api.nlp.controller import nlp_tagger_ns
from app.api.sentiment_price.controller import sentiment_price_ns
from app.api.status.controller import SimpleStatus, DetailedStatus
from app.api.text_analysis.controller import text_analysis_ns
from app.api.text_sources.controller import text_sources_ns
from app.api.text_topics.controller import text_topics_ns
from app.api.texts.controller import texts_ns

api_bp = Blueprint('api', __name__, url_prefix="/api")

# Api definition
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
    }
}

api = Api(api_bp, version="1.0", title="NLP-UTN-FRBA", authorizations=authorizations, security='apikey',
          description="API del TP Nº3 de Procesamiento del Lenguaje Natural - UTN - FRBA",
          default="api", default_label="Available operations"
          )

fetch_job_ns = Namespace("fetch", "Information retrieval jobs")
fetch_job_ns.add_resource(FetchJobPetitionResource, "")
fetch_job_ns.add_resource(FetchJobResource, "/<int:job_id>")

maintenance_ns = Namespace("maintenance", "Application inspection services")
maintenance_ns.add_resource(Endpoints, "/endpoints", endpoint="endpoints")

status_ns = Namespace("status", "Application health-check")
status_ns.add_resource(SimpleStatus, "")
status_ns.add_resource(DetailedStatus, "/detailed")

api.add_namespace(auth_ns)
api.add_namespace(fetch_job_ns)
api.add_namespace(nlp_tagger_ns)
api.add_namespace(texts_ns)
api.add_namespace(sentiment_price_ns)
api.add_namespace(information_retrieval_ns)
api.add_namespace(text_analysis_ns)
api.add_namespace(text_topics_ns)
api.add_namespace(text_sources_ns)
api.add_namespace(crypto_price_ns)
api.add_namespace(maintenance_ns)
api.add_namespace(status_ns)
