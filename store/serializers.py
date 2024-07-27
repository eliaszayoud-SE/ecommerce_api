from rest_framework import serializers
from .models import Category, Item, Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar', 'image', 'date']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'product_id']


class ItemsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'is_favorite', 'category', 'name', 'name_ar', 'description', 'description_ar', 'image', 'count', 'price', 'discount', 'date']

    def get_is_favorite(self, obj):
        favorite_item_ids = self.context.get('favorite_item_ids', set())
        return obj.id in favorite_item_ids
        

class FavoriteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    class Meta:
        model = Favorite
        fields = ['id', 'user_id', 'product_id']

class FavoriteItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Item
        fields = ['id', 'category_id', 'name', 'name_ar', 'description', 'description_ar', 'image', 'count', 'price', 'discount', 'date']