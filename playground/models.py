from django.db import models
import uuid
from .consts import CARS_BRANDS, TRANSMISSION_OPTIONS
from users.models import Profile, Location
from .utils import user_Listing_path
# Create your models here.
class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    brand = models.CharField(max_length=24, choices=CARS_BRANDS, default=None)
    model =models.CharField(max_length=64,)
    vin = models.CharField(max_length=17,)
    mileage = models.IntegerField(default=0)
    color = models.CharField(max_length=24,)
    discription = models.TextField()
    engin = models.CharField(max_length=24,)
    transmission = models.CharField(max_length=24, choices= TRANSMISSION_OPTIONS, default=None)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL,null=True)
    image = models.ImageField(upload_to=user_Listing_path)
    def __str__(self):
        return f'{self.seller.user.username}\'s Listing - {self.model}'
# we add the like list class in here 
class LikeListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.listing.model} listing Liked by {self.profile.user.username}'