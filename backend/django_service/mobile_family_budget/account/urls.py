from django.conf.urls import url, include

from account.views import (
    BudgetGroupListView,
    BudgetGroupUsersListView,
    AddUserUpdateView,
    RefLinkRetrieveUpdateView,
    UserCreateView
)

from mobile_family_budget.utils.ulr_kwarg_consts import GROUP_URL_KWARG

urlpatterns = [
    url(r'^budget-groups/(?P<{}>[0-9]+)/users/'.format(GROUP_URL_KWARG),
        BudgetGroupUsersListView.as_view(), name='budget-group-users'),

    url(r'^budget-groups/(?P<{}>[0-9]+)/invite_link/'.format(GROUP_URL_KWARG),
        RefLinkRetrieveUpdateView.as_view(), name='budget-group-invite-link'),

    url(r'^budget-groups/add-user/', AddUserUpdateView.as_view(), name='add-user'),
    url(r'^budget-groups/', BudgetGroupListView.as_view(), name='budget-groups'),

    url('^api-register/$', UserCreateView.as_view(), name='registration'),
    url(r'^api-auth/', (include('rest_framework.urls', namespace='rest_framework'))),
]
