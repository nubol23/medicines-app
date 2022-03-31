from django.contrib import admin

from apps.remedies.models import Medicine, Purchase

admin.site.register(Medicine)
admin.site.register(Purchase)
