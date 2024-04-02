from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate , login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from .forms import UserForm, LocationForm, ProfileForm
from playground.models import Listing, LikeListing


# Create your views here.

#in here i write how the user log in with her account with the username and password
def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are logged in as {username}')
                return redirect('home')
            else:
                messages.error(request, f'unable to login.')
        else:
            messages.error(request, f'unable to login username or password is incorrect.')
    elif request.method == 'GET':
        login_form = AuthenticationForm()
    return render(request, 'views/login.html', {'login_form': login_form})


# the home path not avalible when you not login 
@login_required
def logout_view(requset):
    logout(requset)
    return redirect('home')


# the register view is the register view page in her we put this in to a user creation form
class RegisterView(View):
    def get(self, request):
        register_form = UserCreationForm()
        return render(request, 'views/register.html',{'register_form':register_form})

    def post(self, request):
        register_form = UserCreationForm( data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request, user)
            messages.success(request, f'user {user.username} registerd successfully.!')
            return redirect('home')
        else:
            messages.error(request, f'unable to register')
            return render(request, 'views/register.html',{'register_form':register_form})
        



# the Profile page in this case you can edit your profile info 
@method_decorator(login_required, name='dispatch')

class ProfileView(View):

    def get(self, request):
        user_listing = Listing.objects.filter(seller=request.user.profile)
        user_liked_Listing = LikeListing.objects.filter(profile=request.user.profile).all()
        user_forms = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        location_form = LocationForm(instance=request.user.profile.location)
        return render(request, 'views/profile.html', {'user_forms':user_forms,
                                                      'profile_form':profile_form,
                                                      'location_form':location_form
                                                      ,'user_listing':user_listing,
                                                      'user_liked_Listing':user_liked_Listing})
    
    def post(self, request):
        user_listing = Listing.objects.filter(seller=request.user.profile)
        user_forms = UserForm(request.POST, instance=request.user)
        user_liked_Listing = LikeListing.objects.filter(profile=request.user.profile).all()
        profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        location_form = LocationForm(request.POST, instance=request.user.profile.location)
        if user_forms.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_forms.save()
            profile_form.save()
            location_form.save()
            messages.success(request, 'Profile Updated Successfully!')
        else:
            messages.error(request, 'Error Updating Profile!')
        return render(request, 'views/profile.html', {'user_forms':user_forms,
                                                      'profile_form':profile_form,
                                                      'location_form':location_form,
                                                      'user_listing':user_listing,
                                                      'user_liked_Listing':user_liked_Listing})