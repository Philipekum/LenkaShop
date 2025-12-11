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


class Collections(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание коллекции')
    is_active = models.BooleanField(default=True, verbose_name='Активная коллекция')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        db_table = 'collection'
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
        ordering = ['-created_at']

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


class Flags(models.Model):
    GROUPS_CHOICES = [
        ('compound-flag', 'Флаг состава'),
        ('product-flag', 'Флаг товара'),
    ]

    title = models.CharField(max_length=150, unique=True, blank=False, verbose_name='Название')
    group = models.CharField(max_length=150, choices=GROUPS_CHOICES, blank=False, verbose_name='Группа')
    is_active = models.BooleanField(default=False, verbose_name='Активен')

    class Meta:
        db_table = 'flags'
        verbose_name = 'Флаг продукта'
        verbose_name_plural = 'Флаги продукта'
    
    def __str__(self):
        return self.title
    

class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    compound = models.TextField(blank=True, null=True, verbose_name='Состав')
    flag = models.ForeignKey(Flags, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Флаг')

    price = models.PositiveIntegerField(default=0, verbose_name='Цена')
    discount_price = models.PositiveBigIntegerField(default=0, verbose_name='Цена по скидке')

    quantity = models.IntegerField(default=0, verbose_name='Количество')

    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    collections = models.ManyToManyField(Collections, blank=True, related_name='products', verbose_name='Коллекции')
    
    laundry_features = models.ManyToManyField(LaundryFeature, blank=True)
    similar_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='similar_to_this', verbose_name='Похожие товары')
    
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
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images', verbose_name='Продукт')
    image = models.ImageField(upload_to='goods_images', verbose_name='Фото')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        db_table = 'product_image'
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фото продуктов'
        ordering = ['order']
        