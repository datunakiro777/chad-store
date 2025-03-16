from rest_framework.routers import DefaultRouter
from users.views import UserViewSet,UserRegisterViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('register', UserRegisterViewSet, basename='register')


urlpatterns = [
    path('', include(router.urls))
]
