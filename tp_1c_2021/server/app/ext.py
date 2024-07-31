from flask_executor import Executor
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from oauthlib.oauth2 import WebApplicationClient

from config import Config

ma = Marshmallow()
migrate = Migrate()
login_manager = LoginManager()
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)
executor = Executor()
