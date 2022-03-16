import os

os.environ["DJANGO_DEBUG"] = "True"

from .default import *  # noqa: E402, F403, F401

ALLOWED_HOSTS += ["localhost", "127.0.0.1"]  # noqa: F405
CORS_ORIGIN_ALLOW_ALL = True
