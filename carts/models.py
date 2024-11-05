from django.db import models
from goods.models import Products


class CartQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0
    

class Cart(models.Model):
    session_key = models.CharField(max_length=32, null=True, blank=True, verbose_name='Сессия')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'cart'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ("id",)

    objects = CartQueryset().as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)
