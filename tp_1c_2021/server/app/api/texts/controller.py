from flask_restx import Resource, Namespace, reqparse

from app.api.schemas import nlp_tagged_text_schema
from app.persistence.text_persistence import text_persistence_service

texts_ns = Namespace("texts", "Analysed texts")

parser = reqparse.RequestParser()
parser.add_argument("limit", default=1, type=int, help="Number of texts to retrieve", required=False)
parser.add_argument("offset", default=0, type=int, help="Number of texts to skip", required=False)


@texts_ns.route("/<string:text_id>")
class TextsResource(Resource):
    # @auth.login_required()
    def get(self, text_id):
        text = text_persistence_service.get_text(text_id)
        if text:
            return nlp_tagged_text_schema.dump(text), 200
        else:
            return {"message": "Text not found"}, 404


@texts_ns.route("")
class TextResource(Resource):
    # @auth.login_required()
    def get(self):
        texts = text_persistence_service.get_all_texts()
        return nlp_tagged_text_schema.dump(texts, many=True), 200


@texts_ns.route("/latests")
class TextResource(Resource):
    # @auth.login_required()
    @texts_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        texts = text_persistence_service.get_last_texts(limit=args["limit"], offset=args["offset"])
        return nlp_tagged_text_schema.dump(texts, many=True), 200


@texts_ns.route("/latests/all-sources")
class TextResource(Resource):
    # @auth.login_required()
    @texts_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        texts = text_persistence_service.get_last_texts_from_all_sources(limit=args["limit"], offset=args["offset"])
        return nlp_tagged_text_schema.dump(texts, many=True), 200
