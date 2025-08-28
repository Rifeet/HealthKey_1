from django.urls import path
from . import views
from .views import request_otp, verify_otp
urlpatterns = [
    path("login/", views.login_view, name="login"),

# authentication/urls.py

    path('request-otp/', request_otp, name='request-otp'),
    path('verify-otp/', verify_otp, name='verify-otp'),
]
