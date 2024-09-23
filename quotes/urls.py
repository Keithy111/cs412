## quotes/urls.py
## description: URL patterns for the quotes app

from django.urls import path  ## library for URLs management
from django.conf import settings  ## configuration package this file will know about the project level sense
from . import views ## be able to use the code in views.py


#all of the URLs that are part of this app

urlpatterns = [
  path(r'quote', views.quote, name="quote"),
  path(r'show_all', views.show_all, name="show_all"),
  path(r'about', views.about, name="about"),
]