from django.conf.urls import url

from account.views import (
    BudgetGroupsListCreateView,
    BudgetGroupUsersListView,
    AddUserUpdateView,
    RefLinkRetrieveUpdateView,
    BudgetGroupRetrieveUpdateView
)

from mobile_family_budget.utils.ulr_kwarg_consts import GROUP_URL_KWARG

urlpatterns = [
    url(r'^budget-groups/(?P<{}>[0-9]+)/users/'.format(GROUP_URL_KWARG),
        BudgetGroupUsersListView.as_view(), name='budget-group-users'),

    url(r'^budget-groups/(?P<{}>[0-9]+)/invite-link/'.format(GROUP_URL_KWARG),
        RefLinkRetrieveUpdateView.as_view(), name='budget-group-invite-link'),

    url(r'^budget-groups/(?P<{}>[0-9]+)/'.format(GROUP_URL_KWARG),
        BudgetGroupRetrieveUpdateView.as_view(), name='budget-group'),

    url(r'^budget-groups/add-user/', AddUserUpdateView.as_view(), name='add-user'),
    url(r'^budget-groups/', BudgetGroupsListCreateView.as_view(), name='budget-groups'),
]
