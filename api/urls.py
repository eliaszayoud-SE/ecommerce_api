from django.urls import path
from . import views

urlpatterns = [
    path('verify_email/', views.activation_user_email),
]