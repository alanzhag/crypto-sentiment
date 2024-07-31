import logging

from flask import request
from werkzeug.exceptions import Forbidden, Unauthorized

from app import db
from app.api.auth.models import WhitelistedUser, User, UserRole
from app.api.auth.token_based.strategy.google_utils import generate_google_flow, USER_INFO_ENDPOINT, \
    get_google_provider_cfg
from app.ext import client
from config import Config

logger = logging.getLogger(__name__)


def get_base_url():
    return request.base_url if Config.DEBUG else request.base_url.replace(Config.LOCALHOST, Config.HOST)


def get_request_uri():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=get_base_url() + "/token",
        scope=["openid", "email", "profile"],
    )
    logger.info(f"Login request uri: {request_uri}")
    return request_uri


def register_token(oauth_response):
    logger.info("A new token is being fetched")
    flow = generate_google_flow()
    flow.redirect_uri = Config.REDIRECT_URI  # should match nuxt redirectUri
    flow.fetch_token(code=oauth_response["code"])
    logger.info("Token fetched")
    session = flow.authorized_session()
    user_info = session.get(USER_INFO_ENDPOINT).json()

    if user_info["email_verified"]:
        unique_id = user_info["sub"]
        user_email = user_info["email"]
        picture = user_info["picture"]
        users_name = user_info["given_name"]
    else:
        raise Unauthorized("User email not available or not verified by Google.")

    if not WhitelistedUser.query.get(user_email):
        raise Unauthorized("User email not allowed")

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=user_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.query.get(unique_id):
        db.session.add(UserRole(user))
        db.session.add(user)
        db.session.commit()

    return flow.credentials
