import uuid

from django.contrib.auth.models import User

from django.utils import timezone

from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    BudgetGroupUserSerializer,
    BudgetGroupSerializer,
    BudgetGroupCreateSerializer,
    AddUserToGroupSerializer,
    RefLinkSerializer
)

from .models import BudgetGroup
from .models import RefLink

from .permissions import IsGroupMember

from purchaseManager.models import PurchaseList


# @method_decorator(csrf_exempt, name='dispatch')
# class AddUserToGroup(View):
#     def get_user_group(self, budget_group, user):
#         budget_group = BudgetGroup.objects.all().get(login=budget_group)
#         if user in budget_group.users.all():
#             return budget_group
#         return None
#
#     def post(self, request):
#         if request.user.is_authenticated():
#             print(request.body)
#             data = json.loads(request.body.decode())
#             link = data['link']
#
#             try:
#                 group = BudgetGroup.objects.get(invite_link=RefLink.objects.get(link=link))
#             except RefLink.DoesNotExist:
#                 print("error")
#                 return HttpResponse(json.dumps({"error": "Ссылка инвалидна"}))
#             group.users.add(request.user)
#             group.save()
#             return HttpResponse(json.dumps({"Status": "Группа добавлена"}))
#
#     def get(self, request):
#         if request.user.is_authenticated():
#             group = self.get_user_group(request.GET.get('budget_group_login'), request.user)
#             if group:
#                 return HttpResponse(json.dumps({"invite_link": group.invite_link.link}))
#             else:
#                 return HttpResponse(json.dumps({"error": "Группа не найдена"}))
def get_error_response(message='invalid link'):
    return Response({'error': '{}'.format(message)}, status=status.HTTP_400_BAD_REQUEST)


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


class BudgetGroupUsersListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    serializer_class = BudgetGroupUserSerializer
    lookup_url_kwarg = 'group_id'

    def get_queryset(self):
        group_id = self.kwargs[self.lookup_url_kwarg]
        group = BudgetGroup.objects.get(id=group_id)
        return group.users.all()


class AddUserUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddUserToGroupSerializer

    def update(self, request, *args, **kwargs):
        """
        Add user to group by invite link
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ref_link = RefLink.objects.get(link=serializer.validated_data.get('link'))
            if ref_link.activation_count <= 0 or timezone.datetime.date(timezone.now()) >= ref_link.expire_date:
                return get_error_response('link was outdated')
            try:
                budget_group = BudgetGroup.objects.get(invite_link=ref_link)
                if budget_group.is_member(request.user):
                    return get_error_response('user is already in this group')
                budget_group.users.add(request.user)
                budget_group.save()
                ref_link.activation_count -= 1
                ref_link.save()
                return Response({'status': 'user successfully added to group {}'.format(budget_group.name)},
                                status=status.HTTP_200_OK)
            except BudgetGroup.DoesNotExist:
                return get_error_response()
        except RefLink.DoesNotExist:
            return get_error_response()


class RefLinkRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    serializer_class = RefLinkSerializer

    def get_queryset(self):
        return RefLink.objects.get(
            budgetgroup=BudgetGroup.objects.get(id=self.kwargs.get('group_id')))

    def get(self, request, *args, **kwargs):
        """
        Retrieve invite link for budget group
        """
        queryset = self.get_queryset()
        return Response(self.get_serializer(queryset).data)

    def update(self, request, *args, **kwargs):
        """
        update expire date or activation count of invite link
        """
        serializer = self.get_serializer(self.get_queryset(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'Invite link data was successfully changed',
                         'expire_date': '{}'.format(serializer.validated_data.get('expire_date')),
                         'activation_count': '{}'.format(serializer.validated_data.get('activation_count'))
                         }, status=status.HTTP_200_OK)


class BudgetGroupListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BudgetGroupCreateSerializer
        return BudgetGroupSerializer

    def get_queryset(self, group_id=None):
        return BudgetGroup.objects.participant(self.request.user.id, group_id)

    def get(self, request, *args, **kwargs):
        """
        Retrieve user groups
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create new group
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        budget_group = serializer.save(owner=request.user)

        budget_group.users.add(request.user)
        invite_link = RefLink(link="{}{}".format(budget_group.id, uuid.uuid4().hex))
        invite_link.save()

        budget_group.invite_link = invite_link
        budget_group.save()

        purchase_list = PurchaseList(budget_group=budget_group)
        purchase_list.save()

        return Response({
            'status': 'group {} successfully registered'.format(budget_group.name)
        },
            status=status.HTTP_201_CREATED)
