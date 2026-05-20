import random

from django.db import models
from django.db.models import QuerySet, Sum, F, Case, When, DecimalField

from goods.models import Products


def generate_unique_order_id() -> int:
    while True:
        order_id = random.randint(100_000_000, 999_999_999)
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id


class DeliveryService(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название службы")
    base_price = models.DecimalField(max_digits=7, decimal_places=2,
                                     verbose_name="Базовая стоимость доставки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        db_table = 'delivery_service'
        verbose_name = 'Служба доставки'
        verbose_name_plural = 'Службы доставки'
        ordering = ('name',)

    def __str__(self):
        return self.name


class OrderItemQueryset(QuerySet):
    def total_price(self) -> float:
        result = self.aggregate(
            total=Sum(
                Case(
                    When(
                        product__discount_price__gt=0,
                        then=F('product__discount_price') * F('quantity')
                    ),
                    default=F('product__price') * F('quantity'),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )
        )['total']
        return float(result) if result is not None else 0.0

    def total_quantity(self) -> int:
        result = self.aggregate(total=models.Sum('quantity'))['total']
        return result or 0


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('canceled', 'Отменен'),
    ]

    session_key = models.CharField(max_length=32, null=True, blank=True,
                                   verbose_name='Сессия')
    order_id = models.BigIntegerField(unique=True, editable=False,
                                      default=generate_unique_order_id)
    created_timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания заказа")

    full_name = models.CharField(max_length=50, default='—',
                                 verbose_name='ФИО')
    email = models.EmailField(verbose_name='e-mail')
    phone_number = models.CharField(max_length=20,
                                    verbose_name="Номер телефона")

    delivery_service = models.ForeignKey(to=DeliveryService,
                                         on_delete=models.PROTECT,
                                         null=True, blank=True,
                                         verbose_name="Служба доставки")
    delivery_address = models.TextField(null=True, blank=True,
                                        verbose_name="Адрес доставки")

    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default='pending', verbose_name="Статус заказа")
    
    def is_paid(self):
        return self.status in ('paid', 'shipped')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('created_timestamp',)

    def __str__(self):
        return f'Заказ № {self.order_id}, Покупатель {self.full_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        related_name="items"
    )
    product = models.ForeignKey(
        to=Products,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Продукт",
        default=None
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")


    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"
        ordering = ("id",)

    objects: OrderItemQueryset = OrderItemQueryset.as_manager() # type: ignore

    @property
    def name(self) -> str:
        return self.product.name if self.product else 'Товар удален'

    @property
    def price(self) -> float:
        return self.product.sell_price() if self.product else 0.0

    def products_price(self) -> float:
        return self.product.sell_price() * self.quantity if self.product else 0.0

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.order_id}"
