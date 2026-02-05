from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

    TYPE_CHOICES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=100)
    category_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name", "category_type")

    def __str__(self):
        return f"{self.name} ({self.category_type})"
