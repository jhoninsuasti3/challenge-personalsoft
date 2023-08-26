"""
Settings of project
"""
from os import getenv as env
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DB_NAME = str(env("DB_NAME", default=""))
DB_USER = str(env("DB_USER", default=""))
DB_PASS = str(env("DB_PASS", default=""))
DB_PORT = str(env("DB_PORT", default=""))
DB_HOST = str(env("DB_HOST", default=""))
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
CELERY_BROKER_URL = str(env("CELERY_BROKER_URL", default=""))
CELERY_RESULT_BACKEND = str(env("CELERY_RESULT_BACKEND", default=""))
