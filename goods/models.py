from django.db import models
from django.core.files.storage import default_storage
from django.templatetags.static import static


class Categories(models.Model):
    name = models.CharField(
        max_length=150, 
        unique=True, 
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        blank=True, 
        null=True, 
        verbose_name='URL',
    )

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Collections(models.Model):
    name = models.CharField(
        max_length=150, 
        unique=True, 
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        blank=True, 
        null=True, 
        verbose_name='URL',
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Описание коллекции',
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Активная коллекция',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания',
    )
    
    class Meta:
        db_table = 'collection'
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name


class CollectionImage(models.Model):
    collection = models.ForeignKey(
        Collections, 
        on_delete=models.CASCADE, 
        related_name='images', 
        verbose_name='Картинка',
    )
    image = models.ImageField(
        upload_to='collection_images', 
        verbose_name='Фото',
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name='Порядок',
    )

    class Meta:
        db_table = 'collection_image'
        verbose_name = 'Фото коллекции'
        verbose_name_plural = 'Фото коллекции'
        ordering = ['order']
    
    def image_exists(self) -> bool:
        if self.image:
            return default_storage.exists(self.image.name)
        return False
    
    def get_image_url_or_default(self, default_path: str='images/No_Image.png') -> str:
        if self.image_exists():
            return str(self.image.url)
        return static(default_path)


class LaundryFeature(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name='Способ стирки',
    )
    icon = models.ImageField(upload_to='laundry_icons')

    class Meta:
        db_table = 'laundry_features'
        verbose_name = 'Способ стирки'
        verbose_name_plural = 'Способы стирки'

    def __str__(self) -> str:
        return self.name


class Flags(models.Model):
    GROUPS_CHOICES = [
        ('compound-flag', 'Флаг состава'),
        ('product-flag', 'Флаг товара'),
    ]

    title = models.CharField(
        max_length=150, 
        unique=True, 
        blank=False, 
        verbose_name='Название',
    )
    group = models.CharField(
        max_length=150, 
        choices=GROUPS_CHOICES, 
        blank=False, 
        verbose_name='Группа',
    )
    is_active = models.BooleanField(
        default=False, 
        verbose_name='Активен',
    )

    class Meta:
        db_table = 'flags'
        verbose_name = 'Флаг продукта'
        verbose_name_plural = 'Флаги продукта'
    
    def __str__(self) -> str:
        return self.title


class Sizes(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS - Extra Small'),
        ('S', 'S - Small'),
        ('M', 'M - Medium'),
        ('L', 'L - Large'),
        ('XL', 'XL - Extra Large'),
    ]

    name = models.CharField(
        max_length=10, 
        choices=SIZE_CHOICES, 
        unique=True, 
        verbose_name='Размер',
    )

    class Meta:
        db_table = 'sizes'
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
    
    def __str__(self) -> str:
        return self.name


class Products(models.Model):
    name = models.CharField(
        max_length=150, 
        unique=True, 
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        blank=True, 
        null=True, 
        verbose_name='URL',
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Описание',
    )
    compound = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Состав',
    )
    flag = models.ForeignKey(
        Flags, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        verbose_name='Флаг',
    )
    sizes = models.ManyToManyField(
        Sizes, 
        blank=True, 
        verbose_name='Размеры',
    )
    price = models.PositiveIntegerField(
        default=0, 
        verbose_name='Цена',
    )
    discount_price = models.PositiveBigIntegerField(
        default=0, 
        blank=True, 
        null=True, 
        verbose_name='Цена по скидке',
    )
    quantity = models.IntegerField(
        default=0, 
        verbose_name='Количество',
    )
    category = models.ForeignKey(
        to=Categories, 
        on_delete=models.CASCADE, 
        verbose_name='Категория',
    )
    collections = models.ManyToManyField(
        Collections, 
        blank=True, 
        related_name='products', 
        verbose_name='Коллекции',
    )
    laundry_features = models.ManyToManyField(
        LaundryFeature, 
        blank=True,
    )
    similar_products = models.ManyToManyField(
        'self', 
        blank=True, 
        symmetrical=False, 
        related_name='similar_to_this', 
        verbose_name='Похожие товары',
    )
    
    def sell_price(self) -> int:
        if self.discount_price and self.discount_price > 0:
            return self.discount_price

        return self.price
    
    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)

    def __str__(self) -> str:
        return f'{self.name}'
    
    def display_id(self) -> int:
        return f'{self.id:05}' # type: ignore


class ProductImage(models.Model):
    product = models.ForeignKey(
        Products, 
        on_delete=models.CASCADE, 
        related_name='images', 
        verbose_name='Продукт',
    )
    image = models.ImageField(
        upload_to='goods_images', 
        verbose_name='Фото',
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name='Порядок',
    )

    class Meta:
        db_table = 'product_image'
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фото продуктов'
        ordering = ['order']
    
    def image_exists(self) -> bool:
        if self.image:
            return default_storage.exists(self.image.name)
        return False
    
    def get_image_url_or_default(self, default_path: str='images/No_Image.png') -> str:
        if self.image_exists():
            return str(self.image.url)
        return static(default_path)
