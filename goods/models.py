from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class LaundryFeature(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Способ стирки')
    icon = models.ImageField(upload_to='laundry_icons')

    class Meta:
        db_table = 'laundry_features'
        verbose_name = 'Способ стирки'
        verbose_name_plural = 'Способы стирки'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    compound = models.TextField(blank=True, null=True, verbose_name='Состав')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True)
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    discount_price = models.PositiveBigIntegerField(default=0, verbose_name='Цена по скидке')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    laundry_features = models.ManyToManyField(LaundryFeature, blank=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name} Кол-во - {self.quantity}'
    
    def display_id(self):
        return f'{self.id:05}'
    