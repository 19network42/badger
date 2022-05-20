import logging
from time import sleep
from authlib.integrations.requests_client import OAuth2Session
from django.conf import settings

from core.celery import app
from .models import User


logger = logging.getLogger(__name__)

client = OAuth2Session(
    client_id=settings.API42_UID,
    client_secret=settings.API42_SECRET,
    token_endpoint='https://api.intra.42.fr/oauth/token',
    scope='public'
)
