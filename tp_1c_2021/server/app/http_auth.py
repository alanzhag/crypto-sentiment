import requests
from flask_httpauth import HTTPTokenAuth

from app.api.auth.models import User
from app.api.auth.token_based.strategy.google_utils import TOKEN_INFO_ENDPOINT

auth = HTTPTokenAuth(scheme='Bearer')


@auth.get_user_roles
def get_user_roles(user):
    return user.role_names


@auth.verify_token
def verify_token(token):
    if not token:
        return None
    response = requests.get(f"{TOKEN_INFO_ENDPOINT}?access_token={token}")
    if not response.ok:
        return None
    user = User.query.get(response.json()["sub"])
    return user if user else None


@auth.error_handler
def auth_error(status):
    return "Forbidden", status
