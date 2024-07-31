import logging

from flask import request
from flask_restx import Resource, Namespace, reqparse

from app.api.auth.token_based.strategy.google_auth_strategy import register_token
from app.api.schemas import user_schema, token_schema
from app.http_auth import auth

auth_ns = Namespace("auth", "Authentication")

parser = reqparse.RequestParser()
parser.add_argument("code", help="Google Oauth code", required=True, location="form")


@auth_ns.route("/me")
class Me(Resource):
    @auth.login_required()
    def get(self):
        return user_schema.dump(auth.current_user()), 200


@auth_ns.route("/token")
class Token(Resource):
    def post(self):
        oauth_response = request.form
        token = register_token(oauth_response)
        if token:
            return token_schema.dump(token), 200
        else:
            return "Unable to fetch token", 500
