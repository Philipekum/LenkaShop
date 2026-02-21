from django.db import models


class ContactInfo(models.Model):
    phone = models.CharField(max_length=20, null=True,
                             verbose_name="Телефон Whatsapp")
    telegram = models.CharField(max_length=50, null=True,
                                verbose_name="Telegram")
    email = models.EmailField(null=True, verbose_name="Email")

    class Meta:
        db_table = 'contact_info'
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контактная информация'

    def __str__(self):
        return f'Контакты: {self.phone}, {self.email}'
