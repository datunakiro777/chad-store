from django.db import models
from django.core.validators import MaxValueValidator
from config.model_utils.models import TimeStampedModel
from products.choices import Currency


class Product(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.GEL)
    tags = models.ManyToManyField("products.ProductTag", related_name='products', blank=True)
    quantity = models.PositiveIntegerField()
    owner = models.ForeignKey('users.User', related_name='owned_products', on_delete=models.CASCADE, null=True, blank=True)

    def average_rating(self):
        pass


class Review(TimeStampedModel, models.Model):
    product = models.ForeignKey('products.Product', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='reviews', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
        unique_together = ['product', 'user']


class FavoriteProduct(TimeStampedModel, models.Model):
    product = models.ForeignKey('products.Product', related_name='favorite_products', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='favorite_products', on_delete=models.SET_NULL, null=True, blank=True)


class ProductTag(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, unique=True)


class Cart(TimeStampedModel, models.Model):
    products = models.ManyToManyField('products.Product', related_name='carts')
    user = models.OneToOneField('users.User', related_name='cart', on_delete=models.SET_NULL, null=True, blank=True)


class ProductImage(TimeStampedModel, models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey('products.Product', related_name='images', on_delete=models.CASCADE)
    

class CartItem(TimeStampedModel, models.Model):
    cart = models.ForeignKey('products.Cart', related_name='user_cart', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name='cart_products', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_of_time_addition = models.FloatField()