from django.contrib import admin
from .models import Listing,LikeListing

class ListingAdmin(admin.ModelAdmin):
    readonly_fields= ('id',)

class LikeListingAdmin(admin.ModelAdmin):
    readonly_fields= ('id',)
    
admin.site.register(Listing, ListingAdmin,)
admin.site.register(LikeListing, LikeListingAdmin,)
# Register your models here.
