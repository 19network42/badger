from dotenv import load_dotenv, find_dotenv
from .celery import app as celery_app


load_dotenv(find_dotenv())

__all__ = ('celery_app',)
