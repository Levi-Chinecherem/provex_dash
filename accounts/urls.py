# accounts/urls.py
from django.urls import path
from .views import signup_view, custom_login_view, logout_view, profile_view, change_password_view, lock_screen_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', custom_login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password_view, name='change_password'),
    path('lock-screen/', lock_screen_view, name='lock_screen'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
