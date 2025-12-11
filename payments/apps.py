from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'
    
    def ready(self):
        from payments.yookassa_config import configure_yookassa
        configure_yookassa()
