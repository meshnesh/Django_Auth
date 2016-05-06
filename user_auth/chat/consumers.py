from base64 import b64decode
import re
import json
import logging

from django.core.cache import cache
from django.core.files.base import ContentFile

from channels import Group
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from channels.sessions import channel_session

from .models import Room, MessagePic, Message

log = logging.getLogger(__name__)

@channel_session
@channel_session_user_from_http
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        prefix, label = message['path'].decode('ascii').strip('/').split('/')
        if prefix != 'chat':
            log.debug('invalid ws path=%s', message['path'])
            return
        room = Room.objects.get(label=label)
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return
    except Room.DoesNotExist:
        log.debug('ws room does not exist label=%s', label)
        return

    log.debug('chat connect room=%s client=%s:%s', 
        room.label, message['client'][0], message['client'][1])
    
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = room.label

@channel_session
@channel_session_user
def ws_message(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, buy room does not exist label=%s', label)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return
    
    # if set(data.keys()) != set(('handle', 'message')):
    #     log.debug("ws message unexpected format data=%s", data)
    #     return


    # if img != None and not MessagePic.objects.filter(
    #     picture__url__exact=img
    #     ).exists():
    #     data['pictures'] = img
    print data.keys()
    if data:
        if  set(data.keys()) == set(('image', 'filename')) and data['image'] != "":
            room = Room.objects.get(label=label)
            base64_img = data['image']
            decoded_img = b64decode(base64_img.partition('base64,')[2])
            img_filename = data['filename']
            img_file = ContentFile(decoded_img, img_filename)
            new_pic = MessagePic.objects.create(
                user=message.user,
                room=room,
                picture=img_file
                )
            new_pic.save()
            current_message = Message.objects.create(
                message="message with picture", 
                pic=new_pic, 
                room=room, 
                handle=message.user.username
                )
            current_message = current_message.as_dict()
            response = {
            'image': new_pic.picture.url,
            'timestamp': current_message['timestamp'],
            'handle': current_message['handle'],
            }

            Group('chat-'+label, channel_layer=message.channel_layer).send({
                'text': json.dumps(response),
                })
        elif set(data.keys()) == set(('handle', 'message')) and data['message'] != "":
            log.debug('chat message room=%s handle=%s message=%s', 
                room.label, data['handle'], data['message'])

            m = room.messages.create(**data)
            data = m.as_dict()

            # See above for the note about Group
            Group('chat-'+label, channel_layer=message.channel_layer).send({
                'text': json.dumps(data),
                })



@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass