from api.models import Scan
from django import forms
from django.forms import ModelForm

class ScanForm(ModelForm):
	class Meta:
		model = Scan
		fields = "__all__"