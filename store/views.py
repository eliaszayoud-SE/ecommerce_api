from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Category, Item, Favorite, Cart
from .serializers import CategorySerializer, ItemsSerializer,CartViewSerializer, FavoriteSerializer, FavoriteItemSerializer, CartSerializer


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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    user_id = request.user.id
    product_id = request.data['product_id']

    favorite = Favorite.objects.filter(user_id=user_id, product_id=product_id)
    if not favorite.exists():
        favorite = Favorite.objects.create(user_id=user_id, product_id=product_id)

    else :
        favorite = favorite.first()

    favorite_serializer = FavoriteSerializer(favorite)
    return Response(favorite_serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favorite(request):
    user_id = request.user.id
    product_id = request.data['product_id']

    
    favorite = Favorite.objects.filter(user_id=user_id, product_id=product_id)
    favorite.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorite(request):
    user_id = request.user.id
    favorite = set(Favorite.objects.filter(user_id=user_id).values_list('product_id',flat=True))

    items = Item.objects.filter(id__in=favorite)
    serializer = FavoriteItemSerializer(items, many=True)
    print(serializer.data)
    return Response({'items':serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user_id = request.user.id
    product_id = request.data['product_id']


    try:
        cart = Cart.objects.get(user_id=user_id, product_id=product_id)
        cart.qty += 1
        cart.save()
    except:
        cart = Cart.objects.create(user_id=user_id, product_id=product_id)
        
    cart_serializer = CartSerializer(cart)
    return Response(cart_serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_from_cart(request):
    user_id = request.user.id
    product_id = request.data['product_id']


    try:
        cart = Cart.objects.get(user_id=user_id, product_id=product_id)
        if(cart.qty> 0):
            cart.qty -= 1
            if(cart.qty==0):
                cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                cart.save()
                cart_serializer = CartSerializer(cart)
                return Response(cart_serializer.data)

        
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            'detali':'No product with the given id'
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])      
def get_count_cart(request):
    user_id = request.user.id
    product_id = request.query_params.get('productId')   

    try:
        cart = Cart.objects.get(user_id=user_id, product_id=product_id)
        return Response({'qty':cart.qty})
        

    except:
        return Response({'qty':0})

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def view_cart(request):
    user_id = request.user.id
    cart =  Cart.objects.select_related('product__category').filter(user_id=user_id)
    
    cart_serializer = CartViewSerializer(cart, many=True)
    total_price = sum([cart['total_price'] for cart in cart_serializer.data])
    total_quantity = sum([cart['qty'] for cart in cart_serializer.data])
    return Response({
            'cart':cart_serializer.data,
            'total_quantity':total_quantity,
            'total_price':total_price
        })
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])     
def search(request):
    search = request.query_params.get('search')
    print(search)
    item = Item.objects.filter(Q(name__icontains=search)|Q(name_ar__icontains=search))
    item_serializer = ItemsSerializer(item, many=True)
    return Response({'items':item_serializer.data})

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def add_address(request):
    user_id = request.user.id
    city = request.data['city']
    street = request.data['street']
    lat = request.data['lat']
    lang = request.data['lang']
    phone = request.data['phone']