from django.contrib import admin

from purchaseManager.models import (
    Purchase,
    PurchaseList
)

admin.site.register(Purchase)
admin.site.register(PurchaseList)

# Register your models here.
