# Generated by Django 5.0.1 on 2024-10-31 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfoPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название страницы')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('content', models.TextField(verbose_name='Контент страницы')),
            ],
            options={
                'verbose_name': 'Информационная страница',
                'verbose_name_plural': 'Информационные страницы',
                'db_table': 'info_page',
            },
        ),
    ]
