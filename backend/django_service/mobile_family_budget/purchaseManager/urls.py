from django.conf.urls import url

from .views import (
    PurchasesListsListCreateApiView,
    PurchaseListRetrieveUpdateView,
    PurchasesListCreateApiView,
    PurchaseRetrieveUpdateView
)

from mobile_family_budget.utils.ulr_kwarg_consts import (
    GROUP_URL_KWARG,
    PURCHASE_LIST_URL_KWARG,
    PURCHASE_URL_KWARG
)

urlpatterns = [
    url(r'group/(?P<{}>[0-9]+)/purchases-lists/(?P<{}>[0-9]+)/purchases/(?P<{}>[0-9]+)/'.format(
        GROUP_URL_KWARG,
        PURCHASE_LIST_URL_KWARG,
        PURCHASE_URL_KWARG),
        PurchaseRetrieveUpdateView.as_view(), name='purchase'),

    url(r'group/(?P<{}>[0-9]+)/purchases-lists/(?P<{}>[0-9]+)/purchases/'.format(GROUP_URL_KWARG,
                                                                                 PURCHASE_LIST_URL_KWARG),
        PurchasesListCreateApiView.as_view(), name='purchases'),
    url(r'group/(?P<{}>[0-9]+)/purchases-lists/(?P<{}>[0-9]+)/'.format(GROUP_URL_KWARG, PURCHASE_LIST_URL_KWARG),
        PurchaseListRetrieveUpdateView.as_view(), name='purchases-list'),

    url(r'group/(?P<{}>[0-9]+)/purchases-lists/'.format(GROUP_URL_KWARG),
        PurchasesListsListCreateApiView.as_view(), name='purchases-lists'),
]
