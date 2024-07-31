import logging
from datetime import datetime
from logging.config import dictConfig

from flask import Flask, jsonify, redirect, request
from flask.cli import with_appcontext
from flask_cors import CORS
from flask_login import current_user
# from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
from werkzeug.exceptions import default_exceptions, HTTPException

from app.db import db
from app.api.fetch.models import FetchJob
from app.api.fetch.services.fetch_job_dispatcher_service import fetch_job_dispatcher_service
from app.api.resources import api_bp
from app.auth.routes import auth_bp
from app.ext import ma, migrate, login_manager, executor
from app.log.logger import LOGGER_CONFIG
from config import Config

dictConfig(LOGGER_CONFIG)

app = Flask(__name__)

# Configuration
app.config.from_object(Config)
app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:3000",
                                                "https://alan-zhao-nlp-utn-frba.herokuapp.com"]}})
logger = logging.getLogger(__name__)

# Define the database object
db.init_app(app)
ma.init_app(app)
executor.init_app(app)
migrate.init_app(app, db)

# Register blueprints
app.register_blueprint(api_bp)
app.register_blueprint(auth_bp)

# User session management setup
login_manager.init_app(app)

# User Role management
# principals = Principal(app)

"""
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user
    # Add the UserNeed to the identity
    if hasattr(current_user, 'email'):
        identity.provides.add(UserNeed(current_user.email))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(str(current_user.roles)))
"""


@app.route("/")
def index():
    return redirect("/api")


@app.cli.command("fetch-job")
def fetch_job_command():
    logging.info(f"Cron fetch job invoked at {datetime.now()}")
    fetch_job: FetchJob = fetch_job_dispatcher_service.synchronic_fetch_job()
    logging.info(f"Id: {fetch_job.id}. Status:{fetch_job.status}. Results: {fetch_job.results}.")
    logging.info(f"Cron fetch job finished at {datetime.now()}")


@app.before_request
def before_request():
    return None  # TODO: Remove later
    doc_url = api_bp.url_prefix
    if request.path in [doc_url, doc_url + "/"] and not (current_user and current_user.is_authenticated):
        logging.warning("Unauthenticated user trying to access swagger docs. Redirecting.")
        return redirect(Config.CURRENT_HOST + "/auth/login")


# Error handling
@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if issubclass(type(e), HTTPException):
        code = e.code
    logger.error(e)
    return jsonify({"status": code, "message": str(e)}), code


for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)

# Build the database:
with app.app_context():
    db.create_all()
