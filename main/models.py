from django.db import models
from django.urls import reverse
from goods.models import Products


class MainPage(models.Model):
    title = models.CharField(max_length=200, default='Главная страница')

    class Meta:
        db_table = 'main_page'
        verbose_name = 'Главная страница'

    def __str__(self):
        return self.title


class MainPageTextBox(models.Model):
    title = models.CharField(max_length=150, blank=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    order = models.PositiveIntegerField(default=0)
    main_page = models.ForeignKey(MainPage, blank=True, null=True, on_delete=models.CASCADE, related_name='text_boxes')

    class Meta:
        db_table = 'main_page_text_box'
        verbose_name = 'Блок текста'
        verbose_name_plural = 'Блоки текста'
        ordering = ['order']
    
    def __str__(self):
        return self.title


class MainPageContentBox(models.Model):
    ALIGNMENT_CHOICES = [
        ('left', 'Слева'),
        ('right', 'Справа'),
    ]

    title = models.CharField(max_length=150, blank=True, verbose_name='Заголовок')
    image1 = models.ImageField(upload_to='main_page_images', verbose_name='Большое фото 1')
    product1 = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_1', verbose_name='Продукт 1')
    product2 = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_2', verbose_name='Продукт 2')
    alignment = models.CharField(max_length=5, choices=ALIGNMENT_CHOICES, default='left', verbose_name='Расположение')
    order = models.PositiveIntegerField(default=0)
    main_page = models.ForeignKey(MainPage, blank=True, null=True, on_delete=models.CASCADE, related_name='content_boxes')

    class Meta:
        db_table = 'main_page_content_box'
        verbose_name = 'Блок контента'
        verbose_name_plural = 'Блоки контента'
        ordering = ['order']

    def __str__(self):
        return self.title


class InfoPage(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название страницы')
    slug = models.SlugField(unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='Контент страницы')

    class Meta:
        db_table = 'info_page'
        verbose_name = 'Информационная страница'
        verbose_name_plural = 'Информационные страницы'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('main:info_page', kwargs={'slug': self.slug})
    