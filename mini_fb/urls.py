## mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfiles  # Import your view class

urlpatterns = [
    path('', ShowAllProfiles.as_view(), name='show_all_profiles'),  # Map '' to ShowAllProfilesView
]
