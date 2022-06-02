from django import forms
from django.forms import ModelForm
from .models import Student, StudentBadge
from api.models import Scan

class ScanForm(ModelForm):
	class Meta:
		model = Scan
		fields = "__all__"

class StudentForm(ModelForm):
	class Meta:
		model = Student
		fields = ('intra_id', 'login', 'email', 'displayname', 'is_staff')

		#to add some style
		labels = {
			'intra_id': '',
			'login': '',
			'email': '',
			'displayname': '',
			'is_staff': '',
		}
		widgets = {
			'intra_id': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Intra_id'}),
			'login': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Login'}),
			'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}),
			'displayname': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Name'}),
			'is_staff': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Staff?'}),
		}
