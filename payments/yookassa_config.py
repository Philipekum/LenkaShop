from yookassa import Configuration
from django.conf import settings


def configure_yookassa() -> None:
    if settings.DEBUG:
        Configuration.configure(
            account_id=settings.YOOKASSA_TEST_SHOP_ID,
            secret_key=settings.YOOKASSA_TEST_SECRET_KEY
        )
    else:
        Configuration.configure(
            account_id=settings.YOOKASSA_SHOP_ID,
            secret_key=settings.YOOKASSA_SECRET_KEY
        )
