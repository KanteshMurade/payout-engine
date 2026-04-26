from django.db import models

class Merchant(models.Model):
    name = models.CharField(max_length=255)

class Payout(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="pending")

class LedgerEntry(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=10)

class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255)
    payout = models.ForeignKey(Payout, on_delete=models.CASCADE)
