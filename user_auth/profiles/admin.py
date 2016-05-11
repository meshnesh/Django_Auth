from django.contrib import admin

from .models import SimplePlace, Skills, Dated, Create_opportunity, UserSkills, RequestApplication, AcceptedRequests, UserProfilePic

# Register your models here.
admin.site.register(SimplePlace)
admin.site.register(Skills)
admin.site.register(Dated)
admin.site.register(Create_opportunity)
admin.site.register(UserSkills)
admin.site.register(RequestApplication)
admin.site.register(AcceptedRequests)
admin.site.register(UserProfilePic)