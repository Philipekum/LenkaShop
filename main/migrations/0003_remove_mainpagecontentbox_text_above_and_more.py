# Generated by Django 5.0.1 on 2024-11-01 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_mainpagetextbox_mainpagecontentbox'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainpagecontentbox',
            name='text_above',
        ),
        migrations.AddField(
            model_name='mainpagecontentbox',
            name='title',
            field=models.CharField(blank=True, max_length=150, verbose_name='Заголовок'),
        ),
    ]