import dj_database_url

from .default import *  # noqa: E402, F403, F401

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(levelname)s] %(asctime)s %(module)s %(name)s.%(funcName)s:%(lineno)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        }
    },
}

DATABASE_URL = os.getenv("DATABASE_URL")  # noqa F405
db_from_env = dj_database_url.config(
    default=DATABASE_URL,
    conn_max_age=500,
    ssl_require=True,
)
DATABASES["default"].update(db_from_env)  # noqa F405
