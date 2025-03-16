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
from products.models import (
    Product,
    Review,
    FavoriteProduct,
    Cart, ProductTag, ProductImage
)
from products.serializers import (
    ProductSerializer,
    ReviewSerializer,
    FavoriteProductSerializer,
    CartSerializer,
    ProductTagSerializer, ProductImageSerializer
    )

from products.permissions import IsObjectOwnerOrReadOnly

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = ProductPaginaton    
    filterset_fields = ['price', 'categories__name']
    search_fields = ['name', 'description']
    throttle_classes = [AnonRateThrottle]



class ReviewViewSet(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user']
    search_fields = []
    
    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_id'])

class FavoriteProductViewSet(ModelViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope ='likes'

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    
class CartViewSet(ListCreateAPIView, GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle]    

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    
class TagList(ListAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_id'])