from django.conf.urls import url

from .views import DeletePurchaseViewSet
from .views import PurchaseViewSet
from .views import (
    PurchasesListsListCreateApiView,
    PurchaseListRetrieveUpdateView,
    PurchasesListCreateApiView
)
from .views import UpdatePurchaseViewSet

from mobile_family_budget.utils.ulr_kwarg_consts import (
    GROUP_URL_KWARG,
    PURCHASE_LIST_URL_KWARG
)

urlpatterns = [
    url(r'group/(?P<{}>[0-9]+)/purchases-lists/(?P<{}>[0-9]+)/purchases'.format(GROUP_URL_KWARG, PURCHASE_LIST_URL_KWARG),
        PurchasesListCreateApiView.as_view(), name='purchases'),
    url(r'group/(?P<{}>[0-9]+)/purchases-lists/(?P<{}>[0-9]+)'.format(GROUP_URL_KWARG, PURCHASE_LIST_URL_KWARG),
        PurchaseListRetrieveUpdateView.as_view(), name='purchases-list'),

    url(r'group/(?P<{}>[0-9]+)/purchases-lists/'.format(GROUP_URL_KWARG),
        PurchasesListsListCreateApiView.as_view(), name='purchases-lists'),

    # deprecated
    url(r'^purchase/', PurchaseViewSet.as_view(), name='new purchase'),
    url(r'^update-purchase/', UpdatePurchaseViewSet.as_view(), name='update purchase'),
    url(r'^delete-purchase/', DeletePurchaseViewSet.as_view(), name='delete purchase'),
]
