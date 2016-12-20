import json

from django.http import HttpResponse
from django.http import QueryDict
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import PurchaseList
from .models import Purchase

from .serializers import PurchaseListSerializer
from .serializers import PurchaseSerializer

from account.models import BudgetGroup


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePurchaseViewSet(View):
    def get_user_group(self, budget_group, user):
        budget_group = BudgetGroup.objects.all().get(login=budget_group)
        if user in budget_group.users.all():
            return budget_group
        return None

    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode())
            budget_group = self.get_user_group(data["budget_group_login"], request.user)
            if BudgetGroup:
                purchase_lists = PurchaseList.objects.filter(budget_group=budget_group)
                for purchase_list in purchase_lists:
                    for purchase in Purchase.objects.filter(purchase_list=purchase_list):
                        if purchase.id == int(data["purchase_id"]):
                            purchase.status = True
                            purchase.save()
                            return HttpResponse(json.dumps({'status': 'Покупка выполнена'}))
                return HttpResponse(json.dumps({'error': 'ID не найден'}))
            else:
                return HttpResponse(json.dumps({'error': 'Группа не найдена'}))


@method_decorator(csrf_exempt, name='dispatch')
class DeletePurchaseViewSet(View):
    def get_user_group(self, budget_group, user):
        budget_group = BudgetGroup.objects.all().get(login=budget_group)
        if user in budget_group.users.all():
            return budget_group
        return None

    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode())
            budget_group = self.get_user_group(data["budget_group_login"], request.user)
            if BudgetGroup:
                purchase_lists = PurchaseList.objects.filter(budget_group=budget_group)
                for purchase_list in purchase_lists:
                    for purchase in Purchase.objects.filter(purchase_list=purchase_list):
                        if purchase.id == int(data["purchase_id"]):
                            purchase.delete()
                            return HttpResponse(json.dumps({'status': 'Покупка  удалена'}))
                return HttpResponse(json.dumps({'error': 'ID не найден'}))
            else:
                return HttpResponse(json.dumps({'error': 'Группа не найдена'}))


@method_decorator(csrf_exempt, name='dispatch')
class PurchaseViewSet(View):
    def get_user_group(self, budget_group, user):
        print(budget_group)
        budget_group = BudgetGroup.objects.all().get(login=budget_group)
        if user in budget_group.users.all():
            return budget_group
        return None

    def post(self, request):
        if request.user.is_authenticated():
            data = json.loads(request.body.decode())
            budget_group = self.get_user_group(data["budget_group_login"], request.user)
            if budget_group:
                components = {
                    'name': data["name"],
                    'count': data["count"],
                    'price': data["price"],
                    'purchase_list': PurchaseList.objects.get(
                        budget_group=BudgetGroup.objects.all().get(login=data["budget_group_login"]))
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
            if budget_group:

                purchase_lists = PurchaseList.objects.filter(budget_group=budget_group)

                purchases = {"purchases": []}

                for purchase_list in purchase_lists:
                    for purchase in Purchase.objects.filter(purchase_list=purchase_list):
                        purchases['purchases'].append(PurchaseSerializer(purchase).data)

                return HttpResponse(json.dumps(purchases))
            else:
                return HttpResponse(json.dumps({'error': 'Группа не найдена'}))
