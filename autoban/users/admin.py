from django.contrib import admin
from autoban.users.models import BaseUser, Profile


admin.site.register(BaseUser)
admin.site.register(Profile)
