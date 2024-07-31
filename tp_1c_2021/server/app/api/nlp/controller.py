from flask_restx import Resource, Namespace, reqparse

from app.api.nlp.services.nlp_tagger_service import nlp_tagger_service
from app.api.schemas import nlp_tagger_response_schema

nlp_tagger_ns = Namespace("nlpTagger", "NLP Tagger - Finds texts and applies NLP to them")

parser = reqparse.RequestParser()
parser.add_argument("source", default=None, help="A specific source to fetch texts from")
parser.add_argument("qty", default=1, type=int, help="Number of text per topic")


@nlp_tagger_ns.route("/run")
class NLPTaggerResource(Resource):
    # @auth.login_required()
    @nlp_tagger_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response = nlp_tagger_service.fetch_and_tag(source=args["source"], qty=args["qty"])
        return nlp_tagger_response_schema.dump(response), 200
