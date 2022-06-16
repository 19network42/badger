import logging
from time import sleep
from authlib.integrations.requests_client import OAuth2Session
from django.conf import settings

from core.celery import app
from accounts.models import User
from .models import Student


logger = logging.getLogger(__name__)

client = OAuth2Session(
	client_id=settings.API42_UID,
	client_secret=settings.API42_SECRET,
	token_endpoint='https://api.intra.42.fr/oauth/token',
	scope='public'
)


@app.task
def update_users():
	try:
		client.fetch_token()
	except:
		logger.critical('Could not authenticate to the API')
		return

	users = User.objects.all()

	for user in users:
		sleep(1)
		req = client.get(
			'https://api.intra.42.fr/v2/users/{}'.format(user.user_id))
		if req.ok:
			json_user = req.json()
			user.login = json_user['login']
			user.email = json_user['email']
			user.first_name = json_user['first_name']
			user.last_name = json_user['last_name']
			user.displayname = json_user['displayname']
			user.image = json_user['image_url']
			user.profile = json_user['url']
			user.is_staff = json_user['staff?']
			user.save()
			logger.debug(
				'User {} was updated'.format(user.user_id))
		else:
			logger.warning(
				'User {} could not be queried from the API'.format(user.user_id))


@app.task
def update_students():
	try:
		client.fetch_token()
	except:
		logger.critical('Could not authenticate to the API')
	page = 0
	student_list = []
	while True:
		req = client.get(
			f'https://api.intra.42.fr/v2/campus/12/users?page[size]=100&page[number]={page}')
		if len(req.json()):
			student_list += req.json()
			page += 1
			sleep(1)
		else:
			break
	for i in student_list:
		if not i['image_url']:
			i['image_url'] = "https://cdn.intra.42.fr/users/default.jpg"

		obj, created = Student.objects.update_or_create(intra_id = i['id'], defaults = {
														"login" : i['login'],
														"email" : i['email'],
														"displayname" : i['displayname'],
														"image_url" : i['image_url'],
														"is_staff" : i['staff?']
															}
														)
	return student_list
