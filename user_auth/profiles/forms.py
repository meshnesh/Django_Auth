import datetime

from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import SimplePlace, Skills,  Dated, Create_opportunity, UserSkills, RequestApplication, Willing_Hour, UserProfilePic

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
		'time',
		]
		widgets = {
		'date': forms.DateTimeInput(attrs={
			'class': 'datepicker'
			}),
		'time': forms.TimeInput(attrs={'class':'timepicker'}),
		}

class HourForm(forms.ModelForm):
	class Meta:
		model = Willing_Hour
		fields = {
		'hours',
		}
		
class UserProfileForm(forms.ModelForm):
    class Meta:
		model = UserProfilePic
		fields = [
		'avatar',       
		]

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


# image

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select an image'
    )
 