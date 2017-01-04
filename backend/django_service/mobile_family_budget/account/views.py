import json

import uuid

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import UserSerializer
from .serializers import GroupSerializer
from .serializers import RefLinkSerializer
from .serializers import BudgetGroupSerializer

from .models import BudgetGroup
from .models import RefLink

from purchaseManager.models import PurchaseList


@csrf_exempt
def authentication(request):
    data = json.loads(request.body.decode())
    username = data['username']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(json.dumps({"sessionid": request.session.session_key}))
    else:
        return HttpResponse(json.dumps({"error": "user not found"}))


@method_decorator(csrf_exempt, name='dispatch')
class Registration(View):
    def post(self, request):
        data = json.loads(request.body.decode())
        username = data['username']
        password = data['password']
        user = User.objects.all().filter(username=username)
        if user:
            return HttpResponse(json.dumps({"error": "user not found"}))
        User.objects.create_user(username=username, password=password)
        print("!")
        return HttpResponse(json.dumps({"status": "success"}))


@method_decorator(csrf_exempt, name='dispatch')
class AddUserToGroup(View):
    def get_user_group(self, budget_group, user):
        budget_group = BudgetGroup.objects.all().get(login=budget_group)
        if user in budget_group.users.all():
            return budget_group
        return None

    def post(self, request):
        if request.user.is_authenticated():
            print(request.body)
            data = json.loads(request.body.decode())
            link = data['link']

            try:
                group = BudgetGroup.objects.get(invite_link=RefLink.objects.get(link=link))
            except RefLink.DoesNotExist:
                print("error")
                return HttpResponse(json.dumps({"error": "Ссылка инвалидна"}))
            group.users.add(request.user)
            group.save()
            return HttpResponse(json.dumps({"Status": "Группа добавлена"}))

    def get(self, request):
        if request.user.is_authenticated():
            group = self.get_user_group(request.GET.get('budget_group_login'), request.user)
            if group:
                return HttpResponse(json.dumps({"invite_link": group.invite_link.link}))
            else:
                return HttpResponse(json.dumps({"error": "Группа не найдена"}))


class CreateUserView(CreateAPIView):
    model = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = self.model.get(username=serializer.data['username'])
        return Response({
            'status': 'user ' + user.username + ' successfully registered'
        },
            status=status.HTTP_201_CREATED, headers=headers
        )


class BudgetGroupListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BudgetGroupSerializer

    def get_queryset(self, **kwargs):
        user_id = self.request.user.id
        return BudgetGroup.objects.participant(user_id, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Retrieve user groups
        """
        if request.GET.get('group_id'):
            queryset = self.get_queryset(**request.GET.dict())
        else:
            queryset = self.get_queryset()
        serializer = BudgetGroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create new group
        """
        return super().post(request, *args, **kwargs)

        # @method_decorator(csrf_exempt, name='dispatch')
        # class BudgetGroupViewSet(generics.):
        # def post(self, request):
        #     if request.user.is_authenticated():
        #         data = json.loads(request.body.decode())
        #         name = data['name']
        #         group_login = data['login']
        #         if BudgetGroup.objects.filter(login=group_login):
        #             return HttpResponse(json.dumps({"error": "Данный логин уже используется"}))
        #
        #         budget_group = BudgetGroup(name=name, login=group_login, group_owner=request.user)
        #         budget_group.save()
        #         budget_group.users.add(request.user)
        #
        #         invite_link = RefLink(
        #             link=str(BudgetGroup.objects.get(login=group_login).id) + str(uuid.uuid1().hex))
        #         invite_link.save()
        #         budget_group.invite_link = invite_link
        #         budget_group.save()
        #         purchase_list = PurchaseList(budget_group=budget_group)
        #         purchase_list.save()
        #
        #         return HttpResponse(json.dumps({"status": "Группа успешно создана"}))
        #     else:
        #         return HttpResponse(json.dumps({"Error": "is not authenticated"}))
        #
        # def get(self, request):
        #     if request.user.is_authenticated():
        #         groups = BudgetGroup.objects.filter(users=request.user)
        #         return HttpResponse(json.dumps({
        #             "Groups": [BudgetGroupSerializer(group).data for group in groups]
        #         }))

        # def update(self, requset):


@method_decorator(csrf_exempt, name='dispatch')
class RefLinkViewSet(viewsets.ModelViewSet):
    queryset = RefLink.objects.all()
    serializer_class = RefLinkSerializer
