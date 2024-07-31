from flask_restx import Resource, Namespace, reqparse

from app.api.information_retrieval.text_fetcher.text_fetcher import text_fetcher
from app.api.schemas import text_fetch_response_schema

information_retrieval_ns = Namespace("informationRetrieval", "Information Retrieval")

parser = reqparse.RequestParser()
parser.add_argument("source", default=None, help="A specific source to fetch texts from")
parser.add_argument("qty", default=1, type=int, help="Number of text per topic")


@information_retrieval_ns.route("")
class InformationRetrieval(Resource):
    # @auth.login_required()
    @information_retrieval_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response = text_fetcher.fetch(source=args["source"], n=args["qty"])
        return text_fetch_response_schema.dump(response), 200
