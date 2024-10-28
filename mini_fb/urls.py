# Author: Keith Yeung 
# Email: keithy@bu.edu 
## mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfiles, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView, CreateFriendView, ShowFriendSuggestionsView
from .views import ShowNewsFeedView

urlpatterns = [
    path(r'', ShowAllProfiles.as_view(), name='show_all_profiles'),  # Map '' to ShowAllProfilesView
    path(r'show_all_profiles/', ShowAllProfiles.as_view(), name="show_all_profiles" ),
    path(r'profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path(r'profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
    path(r'create_profile', CreateProfileView.as_view(), name='create_profile'),
    path(r'profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path(r'status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status_message'),
    path(r'status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status_message'),
    path(r'profile/<int:pk>/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'), 
    path(r'profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path(r'profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),

]
