from .models import LedgerEntry


def get_balance(merchant):
    credit = LedgerEntry.objects.filter(
        merchant=merchant, type="credit"
    ).aggregate(total=models.Sum("amount"))["total"] or 0

    debit = LedgerEntry.objects.filter(
        merchant=merchant, type="debit"
    ).aggregate(total=models.Sum("amount"))["total"] or 0

    return credit - debit