from app.http_auth import auth
from app.log.formatters.request_formatter import RequestFormatter


class AuthRequiredFormatter(RequestFormatter):
    def format(self, record):
        record.user = auth.current_user()["email"] if auth.current_user() else None

        return super().format(record)
