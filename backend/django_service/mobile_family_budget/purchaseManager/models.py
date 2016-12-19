from django.db import models
from account.models import BudgetGroup


class PurchaseList(models.Model):
    name = models.CharField(max_length=30)
    group = models.ForeignKey(BudgetGroup, on_delete=models.CASCADE)


class Purchase(models.Model):
    name = models.CharField(max_length=30)
    count = models.IntegerField(default=1)
    price = models.FloatField()
    current_count = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    trade_list = models.ForeignKey(PurchaseList, on_delete=models.CASCADE)
