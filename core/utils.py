from django.db.models import Sum

def get_balance(merchant):
    total = merchant.ledgerentry_set.aggregate(
        total=Sum("amount")
    )["total"]

    return total or 0