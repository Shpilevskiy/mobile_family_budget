from django.conf.urls import url, include

from rest_framework import routers

from .views import UserViewSet
from .views import GroupViewSet
from .views import CreateUserView

from .views import BudgetGroupViewSet

userRouter = routers.DefaultRouter()
userRouter.register(r'users', UserViewSet)
userRouter.register(r'groups', GroupViewSet)

urlpatterns = [
    url(r'^user/', include(userRouter.urls)),
    url(r'^budget-group/', BudgetGroupViewSet.as_view(), name='new budget group'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('^api-register/$', CreateUserView.as_view()),
]
