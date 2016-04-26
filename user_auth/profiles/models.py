from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from location_field.models.plain import PlainLocationField
# Create your models here.
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
    time = models.TimeField()
        
    def __unicode__(self):
    	return str(self.user)

class Willing_Hour(models.Model):
    user =  models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
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
    hours_required = models.IntegerField(default=0)
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
    def get_absolute_past_url(self):
        return reverse('single_past_request', kwargs={'id':self.id})
        
##################################################################################################################################
class RequestApplication(models.Model):
    user =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    requests = models.ForeignKey(
        Create_opportunity,
        on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.user) + ": " + str(self.requests)

class AcceptedRequests(models.Model):
    user =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    requests = models.ForeignKey(
        Create_opportunity,
        on_delete=models.CASCADE) 


    def __unicode__(self):
        return str(self.user) + ": " + str(self.requests)
        
        
# Images profile

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')