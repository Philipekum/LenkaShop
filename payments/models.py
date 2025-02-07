from django.db import models
from django.utils.timezone import now
from orders.models import Order


class PaymentTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name='Заказ')
    payment_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(default=now, verbose_name='Время оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')  

    class Meta:
        db_table = 'payment_transaction'
        verbose_name = 'Данные об оплате'
        verbose_name_plural = 'Данные об оплатах'

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"
    