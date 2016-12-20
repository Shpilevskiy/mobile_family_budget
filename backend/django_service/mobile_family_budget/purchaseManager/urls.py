from django.conf.urls import url, include

from rest_framework import routers

from .views import PurchaseViewSet
from .views import UpdatePurchaseViewSet
from .views import DeletePurchaseViewSet


urlpatterns = [
    url(r'^purchase/', PurchaseViewSet.as_view(), name='new purchase'),
    url(r'^update-purchase/', UpdatePurchaseViewSet.as_view(), name='update purchase'),
    url(r'^delete-purchase/', DeletePurchaseViewSet.as_view(), name='delete purchase'),
]
