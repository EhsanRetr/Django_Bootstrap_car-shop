from django.urls import path
from .views import home_view, list_view, listing_view, edit_view, like_list_view,msin_page,inquire_listing_view

urlpatterns =[
    path('', msin_page,name='main'),
    path('home/', home_view, name='home'),
    path('list/', list_view,name='list'),
    path('listing/<str:id>/', listing_view ,name='listing'),
    path('listing/<str:id>/edit/',edit_view,name='edit'),
    path('listing/<str:id>/like/',like_list_view ,name='like_listing'),
    path('listing/<str:id>/inquire/',inquire_listing_view ,name='inquire_listing'),
]
