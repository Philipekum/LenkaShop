# Generated by Django 5.0.1 on 2024-11-01 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_mainpagecontentbox_text_above_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainpagecontentbox',
            options={'verbose_name': 'Блок контента', 'verbose_name_plural': 'Блоки контента'},
        ),
        migrations.AlterModelOptions(
            name='mainpagetextbox',
            options={'verbose_name': 'Блок текста', 'verbose_name_plural': 'Блоки текста'},
        ),
        migrations.AlterModelTable(
            name='mainpagecontentbox',
            table='main_page_content_box',
        ),
        migrations.AlterModelTable(
            name='mainpagetextbox',
            table='main_page_text_box',
        ),
    ]