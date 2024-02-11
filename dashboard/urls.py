from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('investment/', views.investment_view, name='investment'),
    path('faq/', views.faq_view, name='faq'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    path('about/', views.about_view, name='about'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
