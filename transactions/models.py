from django.db import models
from django.contrib.auth.models import User
from core.models import Currency


class Transaction(models.Model):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

    TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        related_name="transactions"
    )

    transaction_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT
    )

    amount_in_inr = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False
    )

    date = models.DateField()
    description = models.TextField(blank=True)

    is_refund = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Normalize all amounts to INR for reporting & performance.
        Refunds are stored as negative values internally.
        """
        normalized = self.amount * self.currency.exchange_rate_to_inr

        if self.transaction_type == self.EXPENSE and self.is_refund:
            normalized = -abs(normalized)

        self.amount_in_inr = normalized
        super().save(*args, **kwargs)

# NOTE:
# After saving an EXPENSE transaction, we can check
# if the related budget is exceeded and trigger notifications.

    def __str__(self):
        return f"{self.user} - {self.amount} {self.currency.code}"
