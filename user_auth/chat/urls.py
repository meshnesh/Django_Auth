from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^new(?P<id>[0-9]+)/$', views.new_room, name='new_room'),
    url(r'^rooms/$', views.view_rooms, name='view_rooms'),
    url(r'^volunteer_rooms/$', views.volunteer_view_rooms, name='volunteer_view_rooms'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]