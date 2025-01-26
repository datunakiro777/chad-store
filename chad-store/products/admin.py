from django.contrib import admin
from products.models import (Product, ProductTag, Review, ProductImage, Cart, FavoriteProduct) 

admin.site.register(ProductTag)
admin.site.register(Review)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(FavoriteProduct)

class ImageInLine(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]