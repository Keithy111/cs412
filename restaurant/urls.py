## restaurant/urls.py
## define the URLs for this app

from django.urls import path 
from django.conf import settings
from . import views 

#define a list of valid urls patterns
urlpatterns = [
    path('main/', views.main_page, name="main_page"),  # Main restaurant info page
    path('order/', views.order_page, name="order_page"),  # Online order form page
    path('confirmation/', views.confirmation_page, name="confirmation_page"),  # Order confirmation page
]