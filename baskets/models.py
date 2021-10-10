from django.db import models
from django.utils.functional import cached_property

from users.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def total_quantity(self):
        baskets = self.get_items_cached
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        baskets = self.get_items_cached
        return sum(basket.sum() for basket in baskets)

