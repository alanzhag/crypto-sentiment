import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = FLASK_ENV != "production"
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)
    LOG_LEVEL = "DEBUG" if FLASK_ENV == "development" else "INFO"
    HOST = "https://alan-zhao-nlp-utn-frba.herokuapp.com"
    LOCALHOST = "https://localhost:5000"
    CURRENT_HOST = LOCALHOST if DEBUG else HOST
    REDIRECT_URI = ("http://localhost:3000" if DEBUG else HOST) + "/login"
    ELASTIC_URL = os.environ.get("BONSAI_URL")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///nlp-utn-frba.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    TWEETER_CONSUMER_KEY = os.environ.get("TWEETER_CONSUMER_KEY")
    TWEETER_CONSUMER_SECRET = os.environ.get("TWEETER_CONSUMER_SECRET")
    TWEETER_ACCESS_TOKEN = os.environ.get("TWEETER_ACCESS_TOKEN")
    TWEETER_ACCESS_TOKEN_SECRET = os.environ.get("TWEETER_ACCESS_TOKEN_SECRET")
    REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
    COIN_MARKET_CAP_API_KEY = os.environ.get("COIN_MARKET_CAP_API_KEY")
    X_FREQUENCY = os.environ.get("X_FREQUENCY", 5)
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY")


class FirebaseConfig:
    CERT = {
        "type": "service_account",
        "project_id": "nlp-utn-frba",
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
        "client_email": "firebase-adminsdk-txkok@nlp-utn-frba.iam.gserviceaccount.com",
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-txkok%40nlp-utn-frba.iam.gserviceaccount.com",
    }
