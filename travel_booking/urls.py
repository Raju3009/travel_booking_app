from django.contrib import admin
from django.urls import path, include
from bookings.views import RegisterView, profile_view, home_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('', include('bookings.urls')),
]
