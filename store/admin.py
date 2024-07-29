from django.contrib import admin
from .models import Category, Item, Favorite, Cart
# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Favorite)
admin.site.register(Cart)
