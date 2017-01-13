import uuid

from django.contrib.auth.models import User

from django.db import (
    IntegrityError,
    transaction
)

from django.utils import timezone

from rest_framework import (
    permissions,
    status,
    generics
)
from rest_framework.response import Response

from account.serializers import (
    UserSerializer,
    BudgetGroupUserSerializer,
    BudgetGroupSerializer,
    BudgetGroupCreateSerializer,
    AddUserToGroupSerializer,
    RefLinkSerializer
)

from account.models import (
    BudgetGroup,
    RefLink
)

from account.permissions import IsGroupMember

from purchaseManager.models import PurchaseList

from mobile_family_budget.utils.ulr_kwarg_consts import GROUP_URL_KWARG


def get_error_response(message='invalid link'):
    return Response({'error': '{}'.format(message)}, status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(generics.CreateAPIView):
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
    lookup_url_kwarg = GROUP_URL_KWARG

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
                try:
                    with transaction.atomic():
                        budget_group.save()
                        ref_link.activation_count -= 1
                        ref_link.save()
                except IntegrityError:
                    # TODO: find way to handle errors like this
                    return Response({'error': 'transaction error, try again'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'status': 'user successfully added to group {}'.format(budget_group.name)},
                                status=status.HTTP_200_OK)
            except BudgetGroup.DoesNotExist:
                return get_error_response()
        except RefLink.DoesNotExist:
            return get_error_response()


class RefLinkRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    serializer_class = RefLinkSerializer
    lookup_url_kwarg = GROUP_URL_KWARG

    def get_queryset(self):
        return RefLink.objects.get(
            budgetgroup=BudgetGroup.objects.get(id=self.kwargs.get(GROUP_URL_KWARG)))

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

        try:
            with transaction.atomic():
                budget_group = serializer.save(owner=request.user)

                budget_group.users.add(request.user)
                invite_link = RefLink(link="{}{}".format(budget_group.id, uuid.uuid4().hex))
                invite_link.save()

                budget_group.invite_link = invite_link
                budget_group.save()

                purchase_list = PurchaseList(budget_group=budget_group)
                purchase_list.save()
        except IntegrityError:
            # TODO: find way to handle errors like this
            return Response({'error': 'transaction error, try again'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'status': 'group {} successfully registered'.format(budget_group.name)
        },
            status=status.HTTP_201_CREATED)
