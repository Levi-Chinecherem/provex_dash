# payment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.properties, name='properties'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('agent/', views.agent, name='agent'),
    path('testimonial', views.testimonial, name='testimonial'),
]
