# Author: Keith Yeung 
# Email: keithy@bu.edu 
## mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfiles, ShowProfilePageView, CreateProfileView, CreateStatusMessageView # Import your view class

urlpatterns = [
    path(r'', ShowAllProfiles.as_view(), name='show_all_profiles'),  # Map '' to ShowAllProfilesView
    path(r'profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path(r'profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path(r'create_profile', CreateProfileView.as_view(), name='create_profile'),
]
