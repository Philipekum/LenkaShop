from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'
    verbose_name = 'Оплаты'

    def ready(self) -> None:
        from payments.yookassa_config import configure_yookassa
        configure_yookassa()
