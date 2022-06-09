from django import forms
from django.forms import ModelForm
from .models import Student, StudentBadge, Badge

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

class StudentBadgeForm(ModelForm):
	# student = forms.ModelChoiceField(queryset=Student.objects.filter(pk=student_id))
	# badge = forms.ModelChoiceField(queryset=Badge.objects.filter(pk=badge_id))
	# type = forms.ModelMultipleChoiceField(queryset=None)

	class Meta:
		model = StudentBadge
		fields = ('student', 'badge', 'start_at', 'end_at', 'caution_paid', 'caution_returned', 'lost')

		#to add some style
		labels = {
			'student': 'Student',
			'badge': 'Badge',
			'start_at': 'Start at',
			'end_at': 'End at',
			'caution_paid': 'Caution paid',
			'caution_returned': 'Caution returned',
			'lost': 'Card lost',
		}
		widgets = {
			'student': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'student'}),
			'badge': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'badge'}),
			'start_at': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'start at'}),
			'end_at': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'end at'}),
			'caution_paid': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'caution paid'}),
			'caution_returned': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'caution returned'}),
			'lost': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'card lost'}),
		}
