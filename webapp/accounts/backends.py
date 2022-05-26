from django.contrib.auth.backends import ModelBackend
from authlib.integrations.django_client import OAuth
from django.conf import settings
from .models import User

oauth = OAuth()

oauth.register(
    name='api42',
    client_id=settings.API42_UID,
    client_secret=settings.API42_SECRET,
    access_token_url='https://api.intra.42.fr/oauth/token',
    authorize_url='https://api.intra.42.fr/oauth/authorize',
    api_base_url='https://api.intra.42.fr',
)


class UserBackend(ModelBackend):

	def authenticate(self, request, token=None):
		data = oauth.api42.get('/v2/me', token=token).json()

		# check if user is part of campus 19
		if not any(campus['id'] == 12 for campus in data['campus']):
			return None

		# # check if user is staff member
		# if data['staff?'] == False:
		#     return None

		user, created = User.objects.get_or_create(
			user_id=data['id'],
			defaults={
				'login': data['login'],
				'email': data['email'],
				'first_name': data['first_name'],
				'last_name': data['last_name'],
				'displayname': data['displayname'],
				'image': data['image_url'],
				'profile': data['url'],
				'is_staff': True, # TODO: change for prod
				'is_superuser': True, # TODO: change for prod
			}
		)
		if not created:
			user.login = data['login']
			user.email = data['email']
			user.first_name = data['first_name']
			user.last_name = data['last_name']
			user.displayname = data['displayname']
			user.image = data['image_url']
			user.profile = data['url']
			user.is_staff = data['staff?']
			user.is_superuser = data['staff?']
			user.save()
		return user
