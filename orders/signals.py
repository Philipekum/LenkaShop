from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from orders.models import Order
from django.conf import settings


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance: Order, created, **kwargs):
    if not created:
        return

    subject = f'Заказ №{instance.order_id} успешно оформлен!'

    context = {
        'order': instance,
        # 'site_url': settings.SITE_URL,
    }

    html_message = render_to_string('orders/emails/order_confirmation.html')

    plain_message = f'Здравствуйте, {instance.full_name}! Спасибо за покупку!'

    send_mail(
        subject=subject,
        plain_message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.email],
        html_message=html_message,
        fail_silently=True,
    )
