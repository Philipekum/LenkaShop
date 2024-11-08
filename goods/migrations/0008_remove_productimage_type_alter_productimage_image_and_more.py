# Generated by Django 5.0.1 on 2024-11-07 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0007_alter_productimage_product_alter_productimage_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='type',
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='goods_images', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='layout',
            field=models.CharField(blank=True, choices=[('large', 'Большая'), ('small', 'Маленькая')], max_length=10, null=True, verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='goods.products', verbose_name='Продукт'),
        ),
    ]
