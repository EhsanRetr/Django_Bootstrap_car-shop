from django import forms
from .models import Location, Profile
from django.contrib.auth.models import User
from localflavor.us.forms import  USZipCodeField
from .widgets import CustomPictureFieldWidget


#these thow forms used in profile page field
class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    class Meta:
        model = User
        fields = {'username','first_name','last_name'}



class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(widget=CustomPictureFieldWidget)
    bio = forms.TextInput()
    class Meta:
        model = Profile
        fields = {'photo','bio','phone_number'}


# and this form used in profile and the car list i use a model location for two things 1- user profile 2- car profile
        
class LocationForm(forms.ModelForm):

    class Meta:
        address_1 = forms.CharField(required=True)
        zip_code = USZipCodeField(required=True)
        model = Location
        fields={'address_1','address_2', 'city', 'state', 'zip_code'}

