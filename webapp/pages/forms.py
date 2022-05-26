from django import forms
from django.forms import ModelForm
from .models import Event, Mode

class ModeForm(ModelForm):
	class Meta:
		model = Mode
		fields = ('type', 'amount')

		type : forms.ModelMultipleChoiceField(
			queryset=Mode.objects.all(),
			widget=forms.CheckboxSelectMultiple)
		amount: forms.TextInput(attrs={'class':'form-control', 'placeholder': 'amount'})
	


class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'date', 'end')


		# if we need only certain fields, then:
		# fields = ('date', 'drinks', 'duration', 'name')

		#to add some style
		labels = {
			'name': 'Enter the event name',
			'date': 'Automatically generated date',
			'end': 'End date',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event name'}),
			'date': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Date'}),
			'end': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'End date'}),
		}
