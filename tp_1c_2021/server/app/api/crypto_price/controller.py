from flask_restx import Resource, reqparse, Namespace

from app.api.crypto_price.services.crypto_price_service import crypto_price_service
from app.api.schemas import crypto_price_schema

crypto_price_ns = Namespace("cryptoPrice", "Cryptocurrency prices")

parser = reqparse.RequestParser()
parser.add_argument("symbol", help="Cryptocurrency symbol", required=True)


@crypto_price_ns.route("")
class CryptoPrice(Resource):
    # @auth.login_required()
    @crypto_price_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response = crypto_price_service.get_price(args["symbol"])
        return crypto_price_schema.dump(response), 200
