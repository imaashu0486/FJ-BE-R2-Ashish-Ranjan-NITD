from django.db import models
from django.contrib.auth.models import User


class Budget(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="budgets"
    )

    category = models.ForeignKey(
        "transactions.Category",
        on_delete=models.CASCADE,
        related_name="budgets"
    )

    monthly_limit_in_inr = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    month = models.PositiveIntegerField()  # 1–12
    year = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "category", "month", "year")

    def __str__(self):
        return f"{self.category} - {self.month}/{self.year}"
