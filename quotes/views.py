## quotes/views.py
## description: write view functions to handle URL requests for the quotes app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# List of quotes (3 quotes from the same person)
quotes = [
    "The greatest glory in living lies not in never falling, but in rising every time we fall.",
    "It always seems impossible until it's done.",
    "Education is the most powerful weapon which you can use to change the world."
]

# List of image URLs (3 images of the same person)
images = [
    "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTXM-dBS8rBHChsez_EYDM2vUiqih4yvnZgjMUQyug-aDPjFkKXuS0iqRNTbHNhz1073gHGxGsZUaf-QB8",
    "https://hips.hearstapps.com/hmg-prod/images/_photo-by-per-anders-petterssongetty-images.jpg",
    "https://www.nobelprize.org/images/mandela-13452-content-portrait-mobile-tiny.jpg"
]

# Create your views here.
def quote(request):
  '''function to select random quote and image'''

  random_quote = random.choice(quotes)
  random_image = random.choice(images)
    
    # Pass the selected quote and image to the template
  context = {
      'quote': random_quote,
      'image': random_image
  }
    
  # Render the 'quote.html' template
  return render(request, 'quotes/quote.html', context)

def show_all(request):
    '''Pass all quotes and images to the template'''

    context = {
        'quotes': quotes,
        'images': images
    }
    
    # Render the 'show_all.html' template
    return render(request, 'quotes/show_all.html', context)

def about(request):
    '''Provide information about the person'''

    context = {
        'name': 'Nelson Mandela',
        'bio': 'Nelson Mandela was a South African anti-apartheid revolutionary, political leader, and philanthropist who served as President of South Africa from 1994 to 1999.'
    }
    
    # Render the 'about.html' template
    return render(request, 'quotes/about.html', context)

def redirect_to_quote(request):
    return redirect('/quotes/quote/')

