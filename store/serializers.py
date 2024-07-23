from rest_framework import serializers
from .models import Category, Item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar', 'image', 'date']


class ItemsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Item
        fields = ['id', 'category', 'name', 'name_ar', 'description', 'description_ar', 'image', 'count', 'price', 'discount', 'date']