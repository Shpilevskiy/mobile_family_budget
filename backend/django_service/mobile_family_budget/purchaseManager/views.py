import json

from django.http import HttpResponse
from django.views import View

from .models import PurchaseList
from .models import Purchase

from .serializers import PurchaseListSerializer
from .serializers import PurchaseSerializer

from account.models import BudgetGroup


class PurchaseViewSet(View):
    def get_user_group(self, budget_group, user):
        budget_group = BudgetGroup.objects.all().get(login=budget_group)
        if user in budget_group.users.all():
            return budget_group
        return None

    def post(self, request):
        if request.user.is_authenticated():

            budget_group = self.get_user_group(request.POST.get("budget_group_login"), request.user)
            if budget_group:
                components = {
                    'name': request.POST.get("name"),
                    'count': request.POST.get("count"),
                    'price': request.POST.get("price"),
                    'purchase_status': request.POST.get("status"),
                    'purchase_list': PurchaseList.objects.get(
                        budget_group=BudgetGroup.objects.all().get(login=request.POST.get("budget_group_login")))
                }

                purchase = Purchase(**{k: v for k, v in components.items() if v is not None})
                purchase.save()

                return HttpResponse(json.dumps({'status': 'Покупка создана'}))
            else:
                return HttpResponse(json.dumps({'error': 'Группа не найдена'}))
        else:
            return HttpResponse(json.dumps({'error': 'authentication provided'}))

    def get(self, request):
        if request.user.is_authenticated():

            budget_group = self.get_user_group(request.GET.get("budget_group_login"), request.user)
            purchase_lists = PurchaseList.objects.filter(budget_group=budget_group)

            purchases ={"purchases": []}

            for purchase_list in purchase_lists:
                for purchase in Purchase.objects.filter(purchase_list=purchase_list):
                    print(PurchaseSerializer(purchase).data)
                    purchases['purchases'].append(PurchaseSerializer(purchase).data)

            return HttpResponse(json.dumps(purchases))
