from django.db import models


class Merchant(models.Model):
    name = models.CharField(max_length=100)


class LedgerEntry(models.Model):
    TYPE_CHOICES = (
        ("credit", "Credit"),
        ("debit", "Debit"),
    )

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)


class Payout(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)


class IdempotencyKey(models.Model):
    key = models.CharField(max_length=100, unique=True)
    payout = models.ForeignKey(Payout, on_delete=models.CASCADE, null=True, blank=True)