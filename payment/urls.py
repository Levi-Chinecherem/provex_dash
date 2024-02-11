# payment/urls.py
from django.urls import path
from .views import pricing_view, success_page, fund_view, balance_view

urlpatterns = [
    path('balance/', balance_view, name='balance'),
    path('success/', success_page, name='success_page'),
    path('fund/', fund_view, name='fund'),
    path('pricing/', pricing_view, name='pricing'),
]
