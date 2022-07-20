from api.models import Scan
from django import forms
from django.forms import ModelForm

class ScanForm(ModelForm):
	class Meta:
		model = Scan
		fields = ('uid', 'date', 'mode', 'login', 'validity', 'event')
		labels = {
			'uid': 'UID',
			'date': 'Date',
			'mode': 'Mode',
			'login': 'Login',
			'validity': 'Validity',
			'event': 'Event',
		}
		widgets = {
			'uid': forms.TextInput(attrs={'class':'form-control update_user_table'}),
			'date': forms.TextInput(attrs={'class':'form-control update_user_table'}),
			'mode': forms.TextInput(attrs={'class':'form-control update_user_table'}),
			'login': forms.TextInput(attrs={'class':'form-control update_user_table'}),
			'validity': forms.TextInput(attrs={'class':'form-control update_user_table'}),
			'event': forms.TextInput(attrs={'class':'form-control update_user_table'}),
			}