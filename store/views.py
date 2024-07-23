from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer


@api_view(['GET'])
def home_data(request):
    category = Category.objects.all()
    cartegory_serializer = CategorySerializer(category, many=True)
    
    data = {}
    data['category'] = cartegory_serializer.data
    
    return Response(data)



class CategoryViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

