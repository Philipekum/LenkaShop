# Generated by Django 5.0.1 on 2024-10-31 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_alter_products_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='discount',
        ),
        migrations.AddField(
            model_name='products',
            name='discount_price',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Цена по скидке'),
        ),
    ]
