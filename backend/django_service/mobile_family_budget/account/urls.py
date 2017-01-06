from django.conf.urls import url, include

# from .views import UserViewSet
# from .views import GroupViewSet
from .views import CreateUserView
from .views import AddUserToGroup

from .views import (
    BudgetGroupListView,
    BudgetGroupUsersListView
)

urlpatterns = [
    url(r'^budget-groups/(?P<group_id>[0-9]+)/users/', BudgetGroupUsersListView.as_view()),
    url(r'^budget-groups/', BudgetGroupListView.as_view()),
    # url(r'^budget-groups/(?P<invite_link>)/add/', BudgetGroupListView.as_view()),

    # url(r'^user/', include(userRouter.urls)),
    # url(r'^budget-group/', BudgetGroupViewSet.as_view(), name='new budget group'),
    # url(r'^add-to-group/', AddUserToGroup.as_view(), name='add to group'),
    url(r'^api-auth/', (include('rest_framework.urls', namespace='rest_framework'))),
    url('^api-register/$', CreateUserView.as_view()),
]
