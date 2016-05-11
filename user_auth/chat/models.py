from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse

from PIL import Image

# Create your models here.
def upload_location(instance, filename):
    return "%s%s"%(instance.id, filename)

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField(null=False, blank=False)         
    pic = models.OneToOneField(
        'MessagePic',        
        on_delete=models.CASCADE,
        null=True
        )
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
    
    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}

    def get_absolute_url(self):
        return reverse("chat:chat_room", kwargs = as_dict())

class MessagePic(models.Model):
    room = models.ForeignKey(Room, related_name='pictures', default=None)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
        )
    picture = models.ImageField(
        upload_to = upload_location, 
        null=True,
        blank=True,)   

    def __unicode__(self):
        return self.picture.url
