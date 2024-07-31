import google_auth_oauthlib.flow
import requests

from config import Config

USER_INFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"
TOKEN_INFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/tokeninfo"


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
