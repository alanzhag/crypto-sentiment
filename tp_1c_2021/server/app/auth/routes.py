import json
import logging

import requests
from flask import Blueprint, request, redirect, current_app
from flask_login import login_required, logout_user, login_user, current_user
# from flask_principal import identity_changed, Identity, AnonymousIdentity

from app import db
from app.api.auth.models import User, WhitelistedUser, UserRole
from app.ext import client, login_manager
from config import Config

auth_bp = Blueprint("auth_blueprint", __name__, url_prefix="/auth")
logger = logging.getLogger(__name__)


def get_google_provider_cfg():
    response = requests.get(Config.GOOGLE_DISCOVERY_URL)
    response.raise_for_status()
    return response.json()


def get_base_url():
    return request.base_url if Config.DEBUG else request.base_url.replace(Config.LOCALHOST, Config.HOST)


def get_request_url():
    return request.url if Config.DEBUG else request.url.replace(Config.LOCALHOST, Config.HOST)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth_bp.route("/me")
def me():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<p>Role: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/auth/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.roles, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/auth/login">Google Login</a>'


@auth_bp.route("/login")
def login():
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
    return redirect(request_uri)


@auth_bp.route("/login/callback")
def callback():
    logger.info("Login callback in progress")
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    logger.info(f"Base url: {request.base_url}")
    logger.info(f"New base url: {get_base_url()}")
    logger.info(f"Request url: {request.url}")
    logger.info(f"New request url: {get_request_url()}")

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
    #identity_changed.send(current_app._get_current_object(), identity=Identity(user.email))

    # Send user back to homepage
    return redirect(Config.CURRENT_HOST)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    #identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(Config.CURRENT_HOST + "/auth/me")
