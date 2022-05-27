from django import forms
from django.forms import ModelForm
from .models import Event, Mode

class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'date', 'end')

		# if we need only certain fields, then:
		# fields = ('date', 'drinks', 'duration', 'name')
		# date = forms.DateTimeField()
		# name = forms.CharField()
		# end = forms.DateTimeField()
		# modes = forms.ModelMultipleChoiceField(queryset=Mode.objects.all(), widget=forms.CheckboxSelectMultiple)
		#to add some style
		labels = {
			'name': 'Enter the event name',
			'date': 'Automatically generated date',
			'end': 'End date',
			# 'modes': 'Modes',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event name'}),
			'date': forms.DateInput(attrs={'class':'form-control', 'placeholder': 'Date'}),
			'end': forms.DateInput(attrs={'class':'form-control', 'placeholder': 'End date'}),
			# 'modes': forms.CheckboxSelectMultiple(attrs={'class':'form-control', 'placeholder': 'Modes'})
		}
