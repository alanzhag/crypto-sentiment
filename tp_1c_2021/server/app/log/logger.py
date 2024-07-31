from config import Config

LOGGER_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'auth_formatter': {
            "class": "app.log.formatters.auth_formatter.AuthRequiredFormatter",
            'format': 'User_%(user)s [%(asctime)s] IP_%(remote_addr)s %(levelname)s '
                      'in %(module)s: %(message)s '
        },
        'request_formatter': {
            "class": "app.log.formatters.request_formatter.RequestFormatter",
            'format': '[%(asctime)s] IP_%(remote_addr)s %(levelname)s in %(module)s: %(message)s '
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        "auth": {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'auth_formatter'
        },
        "console": {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'request_formatter'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'request_formatter',
            'filename': "server_log",
            'maxBytes': 1024,
            'backupCount': 3
        }
    },
    "loggers": {
        '': {
            'level': Config.LOG_LEVEL,
            'handlers': ['wsgi', 'file'],
            "propagate": False
        },
        'app': {
            'level': Config.LOG_LEVEL,
            'handlers': ["console", 'file'],
            "propagate": False
        },
        "sqlalchemy": {
            'level': "ERROR",
            'handlers': ["wsgi", 'file'],
            "propagate": False
        },
        "auth_required": {
            'level': 'DEBUG',
            'handlers': ['auth', 'file'],
            'propagate': False
        }
    }
}
