from django.contrib import admin
from .models import TravelOption, Booking

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ("id","type","source","destination","date_time","price","available_seats")
    list_filter = ("type","source","destination")
    search_fields = ("source","destination")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id","user","travel_option","num_seats","total_price","booking_date","status")
    list_filter = ("status","booking_date")
    search_fields = ("user__username",)
