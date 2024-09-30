#restaurant/views.py
from django.shortcuts import render
import random
import time
import datetime


# Create your views here.
def main_page(request):
    # This view only renders the main.html template
    return render(request, 'restaurant/main.html')

def order_page(request):
    # Define a list of potential daily specials
    specials = [
        "Grilled Salmon with Garlic Butter",
        "Spaghetti Bolognese",
        "Chicken Caesar Salad",
        "BBQ Pulled Pork Sandwich",
        "Vegetarian Lasagna",
    ]
    
    # Randomly choose a special
    daily_special = random.choice(specials)

    # Add the daily special to the context dictionary
    context = {
        'daily_special': daily_special,
    }

    # Render the order.html template with the special
    return render(request, 'restaurant/order.html', context=context)

def confirmation_page(request):
    if request.method == 'POST':
        # Retrieve the order details from the form
        items_ordered = request.POST.getlist('items')  # assuming 'items' is a list of item names in the form
        pizza_topping = request.POST.get('toppings')  # Selected topping for pizza
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')

        # Sample prices (in a real app, these would come from a database)
        menu = {
            "Grilled Salmon with Garlic Butter": 20,
            "Spaghetti Bolognese": 15,
            "Chicken Caesar Salad": 12,
            "BBQ Pulled Pork Sandwich": 10,
            "Vegetarian Lasagna": 14,
            'Pizza': 18,  
        }

        # Calculate the total price of the order
        total_price = sum(menu.get(item, 0) for item in items_ordered)

        # Calculate random wait time between 30 and 60 minutes
        wait_time = random.randint(30, 60)
        
        # Get the current time
        current_time = datetime.datetime.now()
        
        # Calculate the ready time by adding wait_time minutes to current_time
        ready_time = current_time + datetime.timedelta(minutes=wait_time)
        
        # Format the ready time to a 12-hour format (e.g., 7:30 PM instead of 19:30)
        ready_time_formatted = ready_time.strftime('%I:%M %p')

        # Create the context for the confirmation page
        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'items_ordered': items_ordered,
            'pizza_topping': pizza_topping,  
            'total_price': total_price,
            'ready_time': ready_time,  # Ready time in HH:MM format
        }

        # Render the confirmation.html template
        return render(request, 'restaurant/confirmation.html', context=context)
