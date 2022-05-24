from django import forms
from django.forms import ModelForm
from .models import Event

class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = "__all__"

		# if we need only certain fields, then:
		# fields = ('date', 'drinks', 'duration', 'name')

		#to add some style
		labels = {
			'name': 'Enter the event name',
			'date': 'Automatically generated date',
			'duration': 'Enter the event duration',
			'drinks': 'Enter the amount of drinks for the event',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event name'}),
			'date': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Date'}),
			'duration': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Duration'}),
			'drinks': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Amout of drinks'}),
		}
