from django.contrib import admin

from .models import (
    RefLink,
    BudgetGroup
)

admin.site.register(RefLink)
admin.site.register(BudgetGroup)
