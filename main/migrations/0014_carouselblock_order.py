# Generated by Django 4.2.16 on 2025-01-26 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_carousel_main_page_carouselblock'),
    ]

    operations = [
        migrations.AddField(
            model_name='carouselblock',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
    ]
