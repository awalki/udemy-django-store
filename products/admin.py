from django.contrib import admin

from products.models import Product, ProductCategory
from users.models import User

admin.site.register(Product)
admin.site.register(User)
admin.site.register(ProductCategory)