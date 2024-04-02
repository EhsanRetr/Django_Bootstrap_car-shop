from django.contrib import admin
from .models import Profile, Location


class profileadmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, profileadmin)
admin.site.register(Location,LocationAdmin)
