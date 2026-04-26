from django.db import models


class Merchant(models.Model):
    name = models.CharField(max_length=100)
    balance = models.IntegerField(default=100000)  # in paise

    def __str__(self):
        return self.name


class Payout(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount_paise = models.IntegerField()
    status = models.CharField(max_length=20)
    idempotency_key = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class IdempotencyKey(models.Model):
    key = models.CharField(max_length=100)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    response_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)