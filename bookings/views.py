from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.views import View

from .models import TravelOption, Booking
from .forms import RegisterForm, ProfileUpdateForm, BookingForm

from django.db.models import Q

def home_redirect(request):
    return redirect('travel_list')

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created!")
            return redirect('travel_list')
        return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'bookings/profile.html', {'form': form})

def travel_list(request):
    qs = TravelOption.objects.all().order_by('date_time')
    q_type = request.GET.get('type', '').strip()
    source = request.GET.get('source', '').strip()
    destination = request.GET.get('destination', '').strip()
    date = request.GET.get('date', '').strip()

    if q_type:
        qs = qs.filter(type=q_type)
    if source:
        qs = qs.filter(source__icontains=source)
    if destination:
        qs = qs.filter(destination__icontains=destination)
    if date:
        qs = qs.filter(date_time__date=date)

    return render(request, 'bookings/travel_list.html', {
        'travels': qs,
        'filters': {'type': q_type, 'source': source, 'destination': destination, 'date': date}
    })

def travel_detail(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)
    form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'travel': travel, 'form': form})

@login_required
def book_travel(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            num_seats = form.cleaned_data['num_seats']
            if num_seats <= 0:
                messages.error(request, "Number of seats must be positive.")
                return redirect('travel_detail', pk=pk)
            if num_seats > travel.available_seats:
                messages.error(request, "Not enough seats available.")
                return redirect('travel_detail', pk=pk)
            total_price = travel.price * num_seats
            booking = Booking.objects.create(
                user=request.user,
                travel_option=travel,
                num_seats=num_seats,
                total_price=total_price,
                status="Confirmed"
            )
            # Deduct seats
            travel.available_seats -= num_seats
            travel.save()
            messages.success(request, f"Booking confirmed (ID: {booking.id})")
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'travel': travel, 'form': form})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == "Cancelled":
        messages.info(request, "Booking already cancelled.")
        return redirect('my_bookings')
    booking.status = "Cancelled"
    booking.save()
    # Restore seats
    travel = booking.travel_option
    travel.available_seats += booking.num_seats
    travel.save()
    messages.success(request, "Booking cancelled and seats restored.")
    return redirect('my_bookings')
