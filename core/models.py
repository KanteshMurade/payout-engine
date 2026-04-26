from django.db import models

class Merchant(models.Model):
    name = models.CharField(max_length=100)


class Payout(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class LedgerEntry(models.Model):
    TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    payout = models.OneToOneField(Payout, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('key', 'merchant')