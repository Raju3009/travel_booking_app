from django.urls import path
from . import views

urlpatterns = [
    path('travels/', views.travel_list, name='travel_list'),
    path('travels/<int:pk>/', views.travel_detail, name='travel_detail'),
    path('travels/<int:pk>/book/', views.book_travel, name='book_travel'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
