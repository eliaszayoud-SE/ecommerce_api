from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('category', views.CategoryViewSet)

urlpatterns = [
    path('home_data/', views.home_data)
]

urlpatterns += router.urls
