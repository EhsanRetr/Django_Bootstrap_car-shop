from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Listing, LikeListing
from .forms import ListingForm
from users.forms import LocationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .filters import ListingFilter
from django.core.mail import send_mail


# Create your views here.


def msin_page(request):
    return render(request, 'views/welcome.html',)









@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    user_liked_listing = LikeListing.objects.filter(profile=request.user.profile).values_list('listing')
    liked_listing_ids = [l[0] for l in user_liked_listing ]
    context ={
        'listing_filter':listing_filter,
        'liked_listing_ids':liked_listing_ids,
    }
    return render(request,'views/home.html', context)














# the django not accept the csrf and now im use @csrf_exempt for that if the django Debug=Fals the @csrf_exempt most be changed

@csrf_exempt
@login_required
def list_view(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST, )
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.loacation = listing_location
                listing.save()
                messages.info(request, f'{listing.model} Listing Posted Successfuly')
                return redirect('home')
            else:
                raise Exception()
        except Exception as e:
            print(e)
            messages.error(request, 'an error occured while posting the listing.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
    return render(request, 'views/list.html',{'listing_form':listing_form, 'location_form':location_form})









# the car View Page i named here Listing 
@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(request, 'views/listing.html', {'listing':listing},)
    except Exception as e:
        messages.error(request, f'invalid UID {id} was provide for listing.')
        return redirect('home')
    










# the car list edit page form 
        
@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method == 'POST':
            listing_form = ListingForm(request.POST, request.FILES , instance=listing)
            location_form = LocationForm(request.POST ,instance=listing.location)
            if listing_form.is_valid and location_form.is_valid :
                location_form.save()
                listing_form.save()
                messages.info(request, f'listing {id} updated Successfully!')
                return redirect('home')
            else:
                messages.error(request, f'an error occured while edit the listing.')
                return reload()
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
        context = {
            'location_form':location_form,
            'listing_form':listing_form
        }
        return render(request, 'views/edit.html',context)
    except Exception as e:
        messages.error(request, f'an error occured while edit the listing.')
        return redirect('home')
    








# the Like View Functionality
def like_list_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    like_lisitng, created = LikeListing.objects.get_or_create(profile=request.user.profile, listing=listing)
    if not created:
        like_lisitng.delete()
    else:
        like_lisitng.save()
    return JsonResponse({
        'is_like_by_user':created,
    })









#i made the email functon here
@login_required
def inquire_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    try:
        emailSubject = f'{request.user.username} is interested in {listing.model}'
        emailmessage = f'hi {listing.seller.user.username},{request.user.username} is interested in your {listing.model} listing on carshop'
        send_mail(
            emailSubject,
            emailmessage,
            'noreply@carshop.com',
            [listing.seller.user.email, ],
            fail_silently=True
        )
        return JsonResponse({
            "success":True
        })
    except Exception as e:
        print(e)
        return JsonResponse({
            "success":False,
            "info":e,
        })