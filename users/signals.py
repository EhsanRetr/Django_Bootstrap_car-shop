from .models import Profile, Location
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def create_profile_Location(sender, instance, created, **kwarg):
    if created:
        profile_Location = Location.objects.create()
        instance.Location = profile_Location
        instance.save()
        
@receiver(post_delete, sender=Profile)
def delete_profile_location(sender, instance, *args, **kwarg):
    if instance.location != None:
        instance.location.delete()