import json

from django.core import serializers

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.views import View

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import UserSerializer
from .serializers import GroupSerializer
from .serializers import RefLinkSerializer
from .serializers import BudgetGroupSerializer

from .models import BudgetGroup
from .models import RefLink


class CreateUserView(CreateAPIView):
    model = User.objects.all()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
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


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class BudgetGroupViewSet(View):
    def post(self, request):
        if request.user.is_authenticated():
            name = request.POST.get('name')
            login = request.POST.get('login')
            if BudgetGroup.objects.filter(login=login):
                return HttpResponse(json.dumps({"error": "Данный логин уже используется"}),
                                    status=412)

            budget_group = BudgetGroup(name=name, login=login, group_owner=request.user)
            budget_group.save()
            budget_group.users.add(request.user)

            return HttpResponse(json.dumps({"status": "Группа успешно создана"}))

    def get(self, request):
        if request.user.is_authenticated():
            groups = BudgetGroup.objects.filter(users=request.user)
            [print(BudgetGroupSerializer(group).data) for group in groups]
            return HttpResponse(json.dumps({
                "Groups": [BudgetGroupSerializer(group).data for group in groups]
            }))


class RefLinkViewSet(viewsets.ModelViewSet):
    queryset = RefLink.objects.all()
    serializer_class = RefLinkSerializer
