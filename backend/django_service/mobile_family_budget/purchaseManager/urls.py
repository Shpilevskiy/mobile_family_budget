from django.conf.urls import url

from .views import (
    PurchasesListsCreateApiView,
    PurchaseListRetrieveUpdateView
)

from .views import PurchaseViewSet
from .views import UpdatePurchaseViewSet
from .views import DeletePurchaseViewSet


urlpatterns = [
    url(r'group/(?P<group_id>[0-9]+)/purchases_lists/', PurchasesListsCreateApiView.as_view()),

    url(r'group/(?P<group_id>[0-9]+)/purchase_list/(?P<purchase_list_id>[0-9]+)', PurchaseListRetrieveUpdateView.as_view()),

    url(r'^purchase/', PurchaseViewSet.as_view(), name='new purchase'),
    url(r'^update-purchase/', UpdatePurchaseViewSet.as_view(), name='update purchase'),
    url(r'^delete-purchase/', DeletePurchaseViewSet.as_view(), name='delete purchase'),
]
