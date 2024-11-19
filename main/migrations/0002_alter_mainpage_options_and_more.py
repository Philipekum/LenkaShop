# Generated by Django 4.2.16 on 2024-11-19 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainpage',
            options={'verbose_name': 'Главная страница', 'verbose_name_plural': 'Главные страницы'},
        ),
        migrations.AlterField(
            model_name='mainpagecontentbox',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.AlterField(
            model_name='mainpagetextbox',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.CreateModel(
            name='MainPageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='main_page_images', verbose_name='Фото')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('content_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.mainpagecontentbox', verbose_name='Контентный блок')),
            ],
            options={
                'verbose_name': 'Фото контентного блока',
                'verbose_name_plural': 'Фото контентных блоков',
                'db_table': 'main_page_images',
                'ordering': ['order'],
            },
        ),
    ]