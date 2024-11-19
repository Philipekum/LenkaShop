# Generated by Django 4.2.16 on 2024-11-18 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название страницы')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('content', models.TextField(verbose_name='Контент страницы')),
                ('position', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Позиция 1'), (2, 'Позиция 2'), (3, 'Позиция 3'), (4, 'Позиция 4'), (5, 'Позиция 5'), (6, 'Позиция 6'), (7, 'Позиция 7'), (8, 'Позиция 8')], null=True, verbose_name='Позиция для отображения')),
            ],
            options={
                'verbose_name': 'Информационная страница',
                'verbose_name_plural': 'Информационные страницы',
                'db_table': 'info_page',
            },
        ),
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Главная страница', max_length=200)),
            ],
            options={
                'verbose_name': 'Главная страница',
                'db_table': 'main_page',
            },
        ),
        migrations.CreateModel(
            name='MainPageTextBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('order', models.PositiveIntegerField(default=0)),
                ('main_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_boxes', to='main.mainpage')),
            ],
            options={
                'verbose_name': 'Блок текста',
                'verbose_name_plural': 'Блоки текста',
                'db_table': 'main_page_text_box',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='MainPageContentBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, verbose_name='Заголовок')),
                ('image1', models.ImageField(upload_to='main_page_images', verbose_name='Большое фото 1')),
                ('alignment', models.CharField(choices=[('left', 'Слева'), ('right', 'Справа')], default='left', max_length=5, verbose_name='Расположение')),
                ('order', models.PositiveIntegerField(default=0)),
                ('main_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='content_boxes', to='main.mainpage')),
                ('product1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_1', to='goods.products', verbose_name='Продукт 1')),
                ('product2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_2', to='goods.products', verbose_name='Продукт 2')),
            ],
            options={
                'verbose_name': 'Блок контента',
                'verbose_name_plural': 'Блоки контента',
                'db_table': 'main_page_content_box',
                'ordering': ['order'],
            },
        ),
    ]