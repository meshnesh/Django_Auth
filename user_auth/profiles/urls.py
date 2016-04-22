from django.conf.urls import patterns, url, include
from django.contrib import admin
from profiles import views

admin.autodiscover()



urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^usertype/$', views.usertype, name="usertype"),
        url(r'^helper/$', views.helper, name="helper"),
        url(r'^seeker/$', views.seeker, name="seeker"),
        url(r'^location/$', views.location, name='location'),
        url(r'^skills/$', views.skills, name='skills'),
        url(r'^days/$', views.days, name='days'),
        url(r'^create/$', views.create_opportunity_form, name = "create"),
        url(r'^browse/$', views.browse, name = "browse"),
        url(r'^commitments/$', views.commitments, name = "commitments"),
        url(r'^commitments/(?P<id>[0-9]+)/$', views.single_commitment, name = "single_commitment"),
        url(r'current/$', views.current_opportunities, name="current_opportunities"),
        url(r'browse/opportunity/(?P<id>[0-9]+)/$', views.helper_request, name="helper_request"),
        url(r'current/opportunity/(?P<id>[0-9]+)/$', views.single_request, name="single_request"),
        url(r'profile/(?P<username>[\w]+)/$', views.view_profile, name="profile"),
        ]