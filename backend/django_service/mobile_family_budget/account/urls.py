from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers

# from .views import UserViewSet
# from .views import GroupViewSet
from .views import CreateUserView
from .views import authentication
from .views import Registration
from .views import AddUserToGroup

# from .views import BudgetGroupViewSet
from .views import BudgetGroupListView

# userRouter = routers.DefaultRouter()
# userRouter.register(r'users', UserViewSet)
# userRouter.register(r'groups', GroupViewSet)

urlpatterns = [
    url(r'^budget-groups/(?P<group_id>\d+)/', BudgetGroupListView.as_view()),
    url(r'^budget-groups/', BudgetGroupListView.as_view()),

    # url(r'^user/', include(userRouter.urls)),
    # url(r'^budget-group/', BudgetGroupViewSet.as_view(), name='new budget group'),
    # url(r'^add-to-group/', AddUserToGroup.as_view(), name='add to group'),
    # url(r'^login/', authentication, name='Authentication'),
    # url(r'^registration/', Registration.as_view(), name='Registration'),
    url(r'^api-auth/', (include('rest_framework.urls', namespace='rest_framework'))),
    url('^api-register/$', CreateUserView.as_view()),
]
