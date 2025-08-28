from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from .models import TravelOption, Booking

class BookingFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass12345")
        self.travel = TravelOption.objects.create(
            type="Flight",
            source="Hyderabad",
            destination="Delhi",
            date_time=timezone.now() + timezone.timedelta(days=1),
            price=1000,
            available_seats=10
        )

    def test_booking_reduces_seats(self):
        self.client.login(username="alice", password="pass12345")
        resp = self.client.post(f"/travels/{self.travel.id}/book/", {"num_seats": 3})
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 7)

    def test_cancel_restores_seats(self):
        self.client.login(username="alice", password="pass12345")
        self.client.post(f"/travels/{self.travel.id}/book/", {"num_seats": 2})
        booking = Booking.objects.first()
        self.client.get(f"/cancel-booking/{booking.id}/")
        self.travel.refresh_from_db()
        self.assertEqual(self.travel.available_seats, 10)
