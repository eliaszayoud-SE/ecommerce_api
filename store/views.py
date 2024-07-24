from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Item
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

class ItemsViewSet(ListModelMixin, GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemsSerializer
