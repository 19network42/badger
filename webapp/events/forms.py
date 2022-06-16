from django import forms
from django.forms import ModelForm
from .models import Event, Mode

class ModeForm(ModelForm):
	# type = forms.CharField(required=False)
	# amount = forms.IntegerField(required=False)
	class Meta:
		model = Mode
		fields = ('type', 'amount')
		labels = {
			'type': 'Enter type of drink/snack',
			'amount': 'Enter its amount',
		}
		widgets = {
			'type': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Drink/snack type', 'required': False}),
			'amount': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Amount', 'required': False}),
		}

class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'date', 'end')
		labels = {
			'name': 'Enter the event name',
			'date': 'Automatically generated date',
			'end': 'End date',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event name'}),
			'date': forms.DateTimeInput(attrs={'class':'form-control', 'placeholder': 'Date'}),
			'end': forms.DateTimeInput(attrs={'class':'form-control', 'placeholder': 'End date'}),
		}