# Generated by Django 5.0.1 on 2024-10-31 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_laundryfeature_products_compound_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='similar_products',
            field=models.ManyToManyField(blank=True, related_name='similar_to_this', to='goods.products', verbose_name='Похожие товары'),
        ),
    ]
