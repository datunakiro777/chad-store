from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from categories.models import Category, CategoryImage
from categories.serializers import CategorySerializer, CategoryDetailSerializer, CategoryImageSerializer

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

class CategoryDetailView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CategoryImageViewSet(ListCreateAPIView):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer
    def get_queryset(self):
        category_id = self.kwargs['category_id']
        
        return self.queryset.filter(category=category_id)
