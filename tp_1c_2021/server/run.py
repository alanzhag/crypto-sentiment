from app import app
from config import Config

context = ("server.cert", "server.key") if Config.DEBUG else None

if __name__ == "__main__":
    app.run(ssl_context=context)
