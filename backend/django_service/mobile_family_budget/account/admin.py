from django.contrib import admin

from account.models import (
    RefLink,
    BudgetGroup
)

admin.site.register(RefLink)
admin.site.register(BudgetGroup)
