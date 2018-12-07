from django.forms import ModelForm,DateTimeInput
from django.contrib.admin import widgets
from django import forms
from cdf import models as cdf_models
class SuggestionForm(forms.ModelForm):

	class Meta:
		model = cdf_models.Suggestions
		fields = ['suggestion','body','status','name','email']

class SecurityReportForm(forms.ModelForm):

	class Meta:
		model = cdf_models.Report
		fields = ['description','image','opinion','geom']

class SecurityEventForm(forms.ModelForm):

	class Meta:
		model = cdf_models.SecurityEvent
		fields = ['title','description','mdate','mtime','geom']

		widgets = {
			'mtime':DateTimeInput(attrs={'type':'time'}),
			'mdate':DateTimeInput(attrs={'type':'date'})

		}

class CommentForm(forms.ModelForm):

    class Meta:
        model = cdf_models.Comment
        fields = ('author', 'text',)

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = cdf_models.ContactUs
		fields = ['fullname','email','phonenumber','body']