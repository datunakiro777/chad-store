from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from django.contrib.auth import get_user_model
from users.models import User
from users.serializer import UserSerializer, RegisterSerializer
from rest_framework.decorators import action
User = get_user_model()


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='me')
    def me(self, request):
        me = self.queryset.filter(user=request.user)
        return me
    

    
class UserRegisterViewSet(CreateModelMixin,GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
