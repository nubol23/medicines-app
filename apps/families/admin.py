from django.contrib import admin

from apps.families.models import Family, FamilyInvitation, Membership

admin.site.register(Family)
admin.site.register(FamilyInvitation)
admin.site.register(Membership)
