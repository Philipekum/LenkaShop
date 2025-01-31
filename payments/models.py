from django.db import models
from django.utils.timezone import now


class Payment(models.Model):
    order_id = models.CharField(max_length=100)  
    payment_id = models.CharField(max_length=100, unique=True)  
    status = models.CharField(max_length=50, default='pending') 
    created_at = models.DateTimeField(default=now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"
