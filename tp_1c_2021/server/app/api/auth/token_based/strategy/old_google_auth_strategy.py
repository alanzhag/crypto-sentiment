import json
import logging

import google_auth_oauthlib.flow
import requests
from flask import request, current_app
from flask_login import login_user, logout_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from app import db
from app.api.auth.models import WhitelistedUser, User, UserRole
from app.ext import client
from config import Config

logger = logging.getLogger(__name__)


def generate_google_flow():
    return google_auth_oauthlib.flow.Flow.from_client_config(
        client_config=get_client_config(),
        scopes=get_client_scopes()
    )


def get_client_scopes():
    return [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid"
    ]


def get_client_config():
    return {
        "web": {
            "client_id": Config.GOOGLE_CLIENT_ID,
            "project_id": "nlp-utn-frba",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": Config.GOOGLE_CLIENT_SECRET,
            "redirect_uris": [
                "https://alan-zhao-nlp-utn-frba.herokuapp.com/auth/login/callback",
                "https://localhost:5000/auth/login/callback",
                "https://127.0.0.1:5000/auth/login/callback",
                "http://localhost:3000/login",
                "https://localhost:5000/api/auth/login/callback"
            ],
            "javascript_origins": [
                "https://127.0.0.1:5000",
                "https://alan-zhao-nlp-utn-frba.herokuapp.com"
            ]
        }
    }


def get_google_provider_cfg():
    response = requests.get(Config.GOOGLE_DISCOVERY_URL)
    response.raise_for_status()
    return response.json()


def get_base_url():
    return request.base_url if Config.DEBUG else request.base_url.replace(Config.LOCALHOST, Config.HOST)


def get_request_url():
    return request.url if Config.DEBUG else request.url.replace(Config.LOCALHOST, Config.HOST)


class GoogleAuthStrategy:
    @staticmethod
    def get_request_uri():
        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=get_base_url() + "/callback",
            scope=["openid", "email", "profile"],
        )
        logger.info(f"Login request uri: {request_uri}")
        return request_uri

    @staticmethod
    def callback():
        logger.info("Login callback in progress")
        # Get authorization code Google sent back to you
        code = request.args.get("code")

        # Find out what URL to hit to get tokens that allow you to ask for
        # things on behalf of a user
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        # Prepare and send a request to get tokens! Yay tokens!
        # request.url/auth/login/callback
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=get_request_url(),
            redirect_url=get_base_url(),  # auth/login/callback
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
        )

        # Parse the tokens!
        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        # You want to make sure their email is verified.
        # The user authenticated with Google, authorized your
        # app, and now you've verified their email through Google!
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            return "User email not available or not verified by Google.", 400

        if not WhitelistedUser.query.get(users_email):
            return "User email not allowed", 403

        # Create a user in your db with the information provided
        # by Google
        user = User(
            id_=unique_id, name=users_name, email=users_email, profile_pic=picture
        )

        # Doesn't exist? Add it to the database.
        if not User.query.get(unique_id):
            db.session.add(UserRole(user))
            db.session.add(user)
            db.session.commit()

        # Begin user session by logging the user in
        login_user(user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.email))

    @staticmethod
    def logout():
        logout_user()
        identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    @staticmethod
    def fetch_token_from_oauth_response(oauth_response):
        logger.info("A new token is being fetched")
        flow = generate_google_flow()
        flow.redirect_uri = Config.REDIRECT_URI  # should match nuxt redirectUri
        try:
            flow.fetch_token(code=oauth_response["code"])
            logger.info("Token fetched")
            session = flow.authorized_session()
            user_info = session.get("https://www.googleapis.com/oauth2/v3/userinfo").json()
            register_user(user_info)
            return flow.credentials
        except Exception as e:
            logger.error("Error fetching token", e)
            return None


def register_user(user_info):
    if user_info["email_verified"]:
        unique_id = user_info["sub"]
        users_email = user_info["email"]
        picture = user_info["picture"]
        users_name = user_info["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    if not WhitelistedUser.query.get(users_email):
        return "User email not allowed", 403

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.query.get(unique_id):
        db.session.add(UserRole(user))
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.email))
