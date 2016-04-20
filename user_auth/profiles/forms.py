from django import forms
from django.utils import timezone
import datetime

from .models import SimplePlace, Skills,  Dated, Create_opportunity, UserSkills, RequestApplication
from django.utils.translation import ugettext_lazy as _

class SingleSkillForm(forms.ModelForm):
	class Meta:
		model = Skills
		fields = [
		'skill'
		]
		
		labels = {
            "skill": _(""),
        }


class PlacedForm(forms.ModelForm):
	class Meta:
		model = SimplePlace
		fields = [
		'location',
		'coordinates',
		'distance_away',
		]
		
class SkillsForm(forms.ModelForm):
	class Meta:
		model = UserSkills
		fields = [
		'skills',
		]
		widgets = {
			'skills': forms.CheckboxSelectMultiple(attrs={'class':'skillsform'}),
		}
		labels = {
            "skills": _("Select Skills Here"),
        }



class DateForm(forms.ModelForm):
	class Meta:
		model = Dated
		fields = [
		'date',
		'hours'
		]
		widgets = {
		'date': forms.DateInput(attrs={
			'class': 'datepicker'
			})
		}
class ApplyForm(forms.ModelForm):
	class Meta:
		model = RequestApplication
		fields = [
		'application'
		]
		widgets = {
		'application': forms.RadioSelect
		}
		
#########################################################################
#frank
class addForm(forms.ModelForm):
    class Meta:
        model = Create_opportunity
        fields = [
        	"image",
            "title",
            "location",
            "coordinates",
            "skills",
            "hours_required",
            "starting_date",
            "stopping_date",
            "starting_time",
            "stopping_time",
            "description",
        ]
        widgets = {
        	'skills': forms.CheckboxSelectMultiple(attrs={'class': 'skillform'}),
        	'starting_date': forms.DateInput(attrs={'class': 'datepicker'}),
        	'stopping_date': forms.DateInput(attrs={'class':'datepicker'}),
        	'starting_time': forms.TimeInput(attrs={'class': 'timepicker'}),
        	'stopping_time': forms.TimeInput(attrs={'class':'timepicker'}),
        }
        
#############################################################################