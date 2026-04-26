from django.db import models

class Merchant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LedgerEntry(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


class Payout(models.Model):
    STATUS_CHOICES = [
        ("pending", "pending"),
        ("processing", "processing"),
        ("completed", "completed"),
        ("failed", "failed"),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    idempotency_key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class IdempotencyKey(models.Model):
    key = models.CharField(max_length=100)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)