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
        url(r'^revive/(?P<id>[0-9]+)/$', views.revive_opportunity, name = "revive_opportunity"),
        url(r'^browse/$', views.browse, name = "browse"),
        url(r'^settings/$', views.settings, name = "settings"),
        url(r'^commitments/$', views.commitments, name = "commitments"),
        url(r'^history/$', views.helper_history, name = "helper_history"),
        url(r'^commitments/(?P<id>[0-9]+)/$', views.single_commitment, name = "single_commitment"),
        url(r'current/$', views.current_opportunities, name="current_opportunities"),
        url(r'past/$', views.past_opportunities, name="past_opportunities"),
        url(r'browse/opportunity/(?P<id>[0-9]+)/$', views.helper_request, name="helper_request"),
        url(r'current/opportunity/(?P<id>[0-9]+)/$', views.single_request, name="single_request"),
        url(r'past/opportunity/(?P<id>[0-9]+)/$', views.single_past_request, name="single_past_request"),
        url(r'history/(?P<id>[0-9]+)/$', views.helper_history_item, name="helper_history_item"),
        url(r'profile/(?P<username>[\w]+)/$', views.view_profile, name="profile"),
        ]