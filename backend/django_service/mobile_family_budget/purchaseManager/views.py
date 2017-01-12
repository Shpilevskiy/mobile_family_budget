import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from .models import PurchaseList
from .models import Purchase

from .serializers import PurchaseSerializer, PurchaseListSerializer

from account.models import BudgetGroup

from account.permissions import IsGroupMember


class PurchasesListsCreateApiView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    serializer_class = PurchaseListSerializer

    def get_serializer_context(self):
        return {'group_id': self.kwargs['group_id']}

    def get_queryset(self):
        return PurchaseList.objects.participant(self.kwargs['group_id'])


class PurchaseListRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    serializer_class = PurchaseListSerializer

    lookup_url_kwarg = 'purchase_list_id'

    def get_queryset(self):
        return PurchaseList.objects.participant(self.kwargs['group_id'], self.kwargs['purchase_list_id'])

    def get_serializer_context(self):
        return {
            'group_id': self.kwargs['group_id'],
            'purchase_list_id': self.kwargs['purchase_list_id']
        }


# only update purchase view
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


# only delete purchase view
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


# get and add purchase view
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
