from django.db import models
from django.urls import reverse

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
    