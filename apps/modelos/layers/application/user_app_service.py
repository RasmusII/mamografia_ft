import logging

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from apps.modelos.models import CustomUser

logger = logging.getLogger(__name__)


class UserAppService:

    @staticmethod
    def get_by_username(username):
        return CustomUser.objects.filter(username=username).first()

    @staticmethod
    def get_by_email(email):
        return CustomUser.objects.filter(email=email).first()

    @classmethod
    def get_user_by_identifier(cls, identifier):
        return cls.get_by_username(identifier) or cls.get_by_email(identifier)