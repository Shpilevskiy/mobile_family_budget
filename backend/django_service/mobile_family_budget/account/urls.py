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
    url(r'^budget-groups/(?P<{}>[0-9]+)/users/'.format(GROUP_URL_KWARG), BudgetGroupUsersListView.as_view()),
    url(r'^budget-groups/(?P<{}>[0-9]+)/invite_link/'.format(GROUP_URL_KWARG), RefLinkRetrieveUpdateView.as_view()),
    url(r'^budget-groups/add-user/', AddUserUpdateView.as_view()),
    url(r'^budget-groups/', BudgetGroupListView.as_view()),

    url(r'^api-auth/', (include('rest_framework.urls', namespace='rest_framework'))),
    url('^api-register/$', UserCreateView.as_view(), name='registration'),
]
