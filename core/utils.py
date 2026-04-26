from django.db.models import Sum

def get_balance(merchant):
    credits = merchant.ledgerentry_set.filter(type='credit').aggregate(Sum('amount'))['amount__sum'] or 0
    debits = merchant.ledgerentry_set.filter(type='debit').aggregate(Sum('amount'))['amount__sum'] or 0
    return credits - debits