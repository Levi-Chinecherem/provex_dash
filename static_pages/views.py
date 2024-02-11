from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "static/index.html")

def properties(request):
    return render(request, "static/property-list.html")

def contact(request):
    return render(request, "static/contact.html")

def about(request):
    return render(request, "static/about.html")

def agent(request):
    return render(request, "static/property-agent.html")

def testimonial(request):
    return render(request, "static/testimonial.html")

