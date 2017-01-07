from django.conf.urls import url, include

# from .views import UserViewSet
# from .views import GroupViewSet
from .views import CreateUserView

from .views import (
    BudgetGroupListView,
    BudgetGroupUsersListView,
    AddUserUpdateView,
    RefLinkRetrieveUpdateView
)

urlpatterns = [
    url(r'^budget-groups/(?P<group_id>[0-9]+)/users/', BudgetGroupUsersListView.as_view()),
    url(r'^budget-groups/(?P<group_id>[0-9]+)/invite_link/', RefLinkRetrieveUpdateView.as_view()),
    url(r'^budget-groups/add-user/', AddUserUpdateView.as_view()),
    url(r'^budget-groups/', BudgetGroupListView.as_view()),

    url(r'^api-auth/', (include('rest_framework.urls', namespace='rest_framework'))),
    url('^api-register/$', CreateUserView.as_view()),
]
