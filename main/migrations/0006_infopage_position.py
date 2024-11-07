# Generated by Django 5.0.1 on 2024-11-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_mainpage_alter_mainpagecontentbox_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='infopage',
            name='position',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Позиция 1'), (2, 'Позиция 2'), (3, 'Позиция 3'), (4, 'Позиция 4'), (5, 'Позиция 5'), (6, 'Позиция 6'), (7, 'Позиция 7'), (8, 'Позиция 8')], null=True, verbose_name='Позиция для отображения'),
        ),
    ]
