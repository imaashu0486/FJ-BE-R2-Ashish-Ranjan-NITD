from django.db.models import Sum
from transactions.models import Transaction
from .models import Budget


def get_spent_amount(user, category, month, year):
    result = Transaction.objects.filter(
        user=user,
        category=category,
        transaction_type=Transaction.EXPENSE,
        date__month=month,
        date__year=year,
    ).aggregate(total=Sum("amount_in_inr"))

    return result["total"] or 0


def is_budget_exceeded(budget: Budget):
    spent = get_spent_amount(
        budget.user,
        budget.category,
        budget.month,
        budget.year,
    )

    return spent > budget.monthly_limit_in_inr, spent
