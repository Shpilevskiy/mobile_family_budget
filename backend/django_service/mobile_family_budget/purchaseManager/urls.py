from django.conf.urls import url

from .views import DeletePurchaseViewSet
from .views import PurchaseViewSet
from .views import (
    PurchasesListsCreateApiView,
    PurchaseListRetrieveUpdateView
)
from .views import UpdatePurchaseViewSet

from mobile_family_budget.utils.ulr_kwarg_consts import (
    GROUP_URL_KWARG,
    PURCHASE_LIST_URL_KWARG
)

urlpatterns = [
    url(r'group/(?P<{}>[0-9]+)/purchases_lists/'.format(GROUP_URL_KWARG), PurchasesListsCreateApiView.as_view()),

    url(r'group/(?P<{}>[0-9]+)/purchase_list/(?P<{}>[0-9]+)'.format(GROUP_URL_KWARG, PURCHASE_LIST_URL_KWARG),
        PurchaseListRetrieveUpdateView.as_view()),

    url(r'^purchase/', PurchaseViewSet.as_view(), name='new purchase'),
    url(r'^update-purchase/', UpdatePurchaseViewSet.as_view(), name='update purchase'),
    url(r'^delete-purchase/', DeletePurchaseViewSet.as_view(), name='delete purchase'),
]
