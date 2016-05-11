from django import forms

from .models import MessagePic

class PicForm(forms.ModelForm):
	class Meta:
		model = MessagePic
		fields = [
		'picture',
		]