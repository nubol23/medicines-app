from django.contrib import admin

from apps.users.models import User, PasswordRestoreRequest

admin.site.register(User)
admin.site.register(PasswordRestoreRequest)
