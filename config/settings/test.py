import os
from pathlib import Path

import dotenv

# Setup test environment variables
BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv.load_dotenv(f"{BASE_DIR}/.env")

os.environ["DJANGO_DEBUG"] = "True"
os.environ["DJANGO_TESTING"] = "True"

from .default import *  # noqa: E402, F403, F401

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME", "medicines"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASS"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", 5432),
        "ATOMIC_REQUESTS": True,
        "TEST": {"NAME": "test_medicines"},
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"

print("SETUP TEST")
