from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('category', views.CategoryViewSet)
router.register('item', views.ItemsViewSet)
# router.register('favorite', views.FavoriteViewSet)

urlpatterns = [
    path('home_data/', views.home_data),
    path('add_favorite/', views.add_favorite),
    path('delete_favorite/', views.delete_favorite)
]

urlpatterns += router.urls
