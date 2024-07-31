from flask import current_app, url_for, request
from flask_restx import Resource

from app.api.auth.models import RoleName
from app.http_auth import auth
from config import Config


class Endpoints(Resource):
    @auth.login_required(role=RoleName.ADMIN.name)
    def get(self):
        endpoints = {"links": {}}
        for rule in current_app.url_map.iter_rules():
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                base = Config.HOST if Config.FLASK_ENV == 'production' else request.host_url[:-1]
                endpoints["links"][rule.endpoint] = base + url
        return endpoints


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)
