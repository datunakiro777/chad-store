from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from django.contrib.auth import get_user_model
from users.models import User
from users.serializer import UserSerializer, RegisterSerializer

User = get_user_model()


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
class UserRegisterViewSet(CreateModelMixin,GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
