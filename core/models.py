from django.db import models

class Merchant(models.Model):
    name = models.CharField(max_length=100)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Payout(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"{self.id} - {self.status}"