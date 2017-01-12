from django.conf.urls import url

from .views import PurchaseListCreateApiView

from .views import PurchaseViewSet
from .views import UpdatePurchaseViewSet
from .views import DeletePurchaseViewSet


urlpatterns = [
    url(r'group/(?P<group_id>[0-9]+)/purchase_lists/', PurchaseListCreateApiView.as_view()),
    url(r'^purchase/', PurchaseViewSet.as_view(), name='new purchase'),
    url(r'^update-purchase/', UpdatePurchaseViewSet.as_view(), name='update purchase'),
    url(r'^delete-purchase/', DeletePurchaseViewSet.as_view(), name='delete purchase'),
]
