# payment/urls.py
from django.urls import path
from .views import withdraw_view, pricing_view, success_page, fund_view, balance_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('balance/', balance_view, name='balance'),
    path('success/', success_page, name='success_page'),
    path('fund/', fund_view, name='fund'),
    path('pricing/', pricing_view, name='pricing'),
    path('withdraw/', withdraw_view, name='withdraw'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
