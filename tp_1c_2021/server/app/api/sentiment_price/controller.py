from flask import request
from flask_restx import Resource, Namespace, reqparse, fields

from app.api.schemas import sentiment_price_snapshot_schema, computed_sentiment_price_schema, \
    sentiment_price_source_schema
from app.api.sentiment_price.service.sentiment_price_service import sentiment_price_service
from app.persistence.sentiment_price_persistence import sentiment_price_persistence_service

sentiment_price_ns = Namespace("sentimentPrice", "Peek the sentiment and price associated with every crypto")

parser = reqparse.RequestParser()
parser.add_argument("last", default=1, type=int, help="Number of snapshots to retrieve")

sentiment_model = sentiment_price_ns.schema_model('Sentiment', {
    "enum": ["POSITIVE", "NEUTRAL", "NEGATIVE"],
    "type": 'string'
})

sentiment_price_source_model = sentiment_price_ns.model('SentimentPriceSource', {
    "source": fields.String,
    "symbol": fields.String,
    "price": fields.Float,
    "sentiment": fields.Nested(sentiment_model)
})

resource_fields = sentiment_price_ns.model('SentimentPriceCalculatorInput', {
    "input": fields.List(fields.Nested(sentiment_price_source_model))
})


@sentiment_price_ns.route("/compute")
class SentimentPriceCalculatorResource(Resource):
    # @auth.login_required()
    @sentiment_price_ns.expect(resource_fields)
    def post(self):
        data = request.get_json()
        sentiment_price_source_list = sentiment_price_source_schema.load(data["input"], many=True)
        response = sentiment_price_service.generate_sentiment_price_snapshot(sentiment_price_source_list)
        return computed_sentiment_price_schema.dump(response), 200


@sentiment_price_ns.route("/snapshot")
class SentimentPriceSnapshotListResource(Resource):
    # @auth.login_required()
    @sentiment_price_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response = sentiment_price_persistence_service.get_last_n_snapshots(n=args["last"])
        return sentiment_price_snapshot_schema.dump(response, many=True), 200


@sentiment_price_ns.route("/<string:snapshot_id>")
class SentimentPriceSnapshotResource(Resource):
    # @auth.login_required()
    def get(self, snapshot_id):
        snapshot = sentiment_price_persistence_service.get_snapshot(snapshot_id)
        if snapshot:
            return sentiment_price_snapshot_schema.dump(snapshot), 200
        else:
            return {"message": "Sentiment-Price snapshot not found"}, 404
