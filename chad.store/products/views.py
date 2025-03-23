from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from products.pagination import ProductPaginaton
from rest_framework.throttling import ScopedRateThrottle, AnonRateThrottle
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from products.models import (
    Product,
    Review,
    FavoriteProduct,
    Cart, ProductTag, ProductImage, CartItem
)
from products.serializers import (
    ProductSerializer,
    ReviewSerializer,
    FavoriteProductSerializer,
    CartSerializer,
    ProductTagSerializer, ProductImageSerializer, CartItemSerializer
    )

from products.permissions import IsObjectOwnerOrReadOnly

class ProductViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories', 'price']

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def my_product(self, request):
        owned_products = request.user.owned_products.all()
        return owned_products
    
    
    
class ReviewViewSet(ListModelMixin, CreateModelMixin, GenericViewSet, DestroyModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if request.user != review.user:
            raise PermissionError
        return self.destroy(request, *args, **kwargs)
    
class FavoriteProductViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product__name']

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    
class CartViewSet(ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    
class TagList(ListModelMixin, GenericViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]

class ProductImageViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_id'])
    

class CartItemView(GenericViewSet, DestroyModelMixin, CreateModelMixin, ListModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)