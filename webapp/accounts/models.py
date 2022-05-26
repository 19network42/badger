from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):

	def _create_user(self, user_id, login, email, **extra_fields):
		user = self.model(
			user_id=user_id,
			login=login,
			email=email,
			**extra_fields
		)
		user.save()
		return user

	def create_user(self, login, email):
		pass


class User(AbstractBaseUser, PermissionsMixin):

	user_id = models.IntegerField(unique=True, primary_key=True)
	login = models.CharField(max_length=255, unique=True)
	email = models.EmailField()

	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	displayname = models.CharField(max_length=255)

	image = models.URLField()
	profile = models.URLField()

	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	password = None

	USERNAME_FIELD = 'login'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = ['user_id', 'displayname', 'email', 'profile', 'image']

	def get_full_name(self):
		return self.displayname

	def get_short_name(self):
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def __str__(self):
		return self.login
