from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category, Item, Favorite
from .serializers import CategorySerializer, ItemsSerializer


@api_view(['GET'])
def home_data(request):
    categories = Category.objects.all()
    cartegory_serializer = CategorySerializer(categories, many=True)

    items = Item.objects.exclude(discount=0)
    item_serializer = ItemsSerializer(items, many=True)

    
    data = {}
    data['categories'] = cartegory_serializer.data
    data['items'] = item_serializer.data
    
    return Response(data)



class CategoryViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ItemsViewSet(ListModelMixin, GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.request.query_params.get('categoryId')
        return Item.objects.filter(category_id=category_id).all()
    
    def get_serializer_context(self):
        favorite_item_ids = set()
        print(self.request.user)
        if self.request.user.is_authenticated:

            favorite_item_ids = set(Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True))

        return {
            'favorite_item_ids':favorite_item_ids
        }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'items':serializer.data})