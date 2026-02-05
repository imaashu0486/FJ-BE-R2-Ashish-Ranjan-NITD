from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)  # INR, USD
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    exchange_rate_to_inr = models.DecimalField(
        max_digits=10, decimal_places=4
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}"
