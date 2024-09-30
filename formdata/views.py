## formdata/views.py 
## get the form to display as "main" web page for this app:

from django.shortcuts import render
# Create your views here.
def show_form(request):
  '''Show the web page with the form.'''

  template_name = "formdata/show_form.html"
  return render(request, template_name)

def submit(request):
  '''Process the form submission, and generate a result.'''
  template_name = "formdata/confirmation.html"

  # check that we have a POST request:
  if request.POST:
      # read the form data into python variables:
      name = request.POST['name']
      favorite_color = request.POST['favorite_color']

      #package the form data up as context variables for the template
      context = {
          'name': name,
          'favorite_color':  favorite_color,
            
      }
  return render(request, template_name, context=context)

  return redirect("show_form")
