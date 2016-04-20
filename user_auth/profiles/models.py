from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.conf import settings

# Kiilus imports
from django.core.urlresolvers import reverse
from location_field.models.plain import PlainLocationField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
# Create your models here.
# Create your models here.
class profile(models.Model):
	name = models.CharField(max_length = 1200)
	description = models.TextField(default = 'description default')
	
	def __unicode__(self):
		return self.name
		
		
		
# class Opportunity(models.Model):
# 	user = models.ForeignKey(
# 	    settings.AUTH_USER_MODEL,
# 	    on_delete=models.CASCADE,
# 	    )
# 	title = models.CharField(max_length=120)
# 	image = models.ImageField(null=True, blank=True)
# 	description = models.TextField()
# 	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	
	
# 	def __str__(self):
# 		return self.title


# 	def __unicode__(self):
# 		return self.title
#===============================================
# Kiilu
class Skills(models.Model):
    skill = models.CharField(max_length=255)
    def __unicode__(self):
        return self.skill

class SimplePlace(models.Model):
    user =  models.OneToOneField(
	    settings.AUTH_USER_MODEL,
	    on_delete=models.CASCADE,
	    primary_key=True,
	    )
    distance_away = models.IntegerField(default=0,  validators=[MinValueValidator(0)])
    location = models.CharField(max_length=255)
    coordinates = PlainLocationField(based_fields=['location'], zoom=7)

    def __unicode__(self):
    	return self.location

    def get_absolute_url(self):
		return reverse("page", kwargs={"id": self.id})
		
    def clean(self):
        if self.distance_away < 0:
            raise ValidationError(_('Only numbers equal to 0 or greater are accepted.'))

class UserSkills(models.Model):
    user =  models.OneToOneField(
	    settings.AUTH_USER_MODEL,
	    on_delete=models.CASCADE,
	    primary_key=True,
	    )
    skills = models.ManyToManyField(Skills)
    
    def __unicode__(self):
    	return str(self.user)

class Dated(models.Model):
    user =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    date = models.DateField()
    hours = models.IntegerField(default=0)
    
    def __unicode__(self):
    	return str(self.user)

#=======================================================

#########################################################
#frank
# models for creating opportunity
class Create_opportunity(models.Model):
    user =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    image = models.ImageField(upload_to='static/image', verbose_name='My Photo', blank = True, default = 0)
    title = models.CharField(max_length=140)
    location = models.CharField(max_length=255)
    coordinates = PlainLocationField(based_fields=['location'], zoom=7)
    description = models.TextField(null=True)
    skills = models.ManyToManyField(Skills)
    hours_required = models.CharField(max_length=140, blank = True)
    starting_time = models.TimeField()
    stopping_time = models.TimeField()
    starting_date = models.DateField()
    stopping_date = models.DateField()
    created_date = models.DateTimeField(
            default=timezone.now
            )

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('single_request', kwargs={'id': self.id})
    def get_absolute_helper_url(self):
        return reverse('helper_request', kwargs={'id': self.id})
    def get_absolute_chat_url(self):
        return reverse('chat:new_room', kwargs={'id': self.id})
        
##################################################################################################################################
class RequestApplication(models.Model):
    user =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    requests = models.OneToOneField(
        Create_opportunity,
        on_delete=models.CASCADE)
    application = models.BooleanField()

    def __unicode__(self):
        return str(self.user) + ": " + str(self.requests)