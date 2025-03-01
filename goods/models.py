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
    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    discount_price = models.PositiveBigIntegerField(default=0, verbose_name='Цена по скидке')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    laundry_features = models.ManyToManyField(LaundryFeature, blank=True)
    similar_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='similar_to_this', verbose_name='Похожие товары')
    options = models.ManyToManyField('self', blank=True, symmetrical=True, verbose_name='Товары-варианты')
    
    def sell_price(self):
        if self.discount_price > 0:
            return self.discount_price

        return self.price
    
    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name}'
    
    def display_id(self):
        return f'{self.id:05}'


class ProductImage(models.Model):
    LAYOUT_CHOICES = [
        ('large', 'Большая'),
        ('small', 'Маленькая'),
    ]

    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images', verbose_name='Продукт')
    image = models.ImageField(upload_to='goods_images', verbose_name='Фото')
    layout = models.CharField(max_length=10, choices=LAYOUT_CHOICES, blank=True, null=True, verbose_name='Размер')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        db_table = 'product_image'
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фото продуктов'
        ordering = ['order']
        