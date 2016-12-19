from django.conf.urls import url, include

from rest_framework import routers

from .views import PurchaseViewSet


urlpatterns = [
    url(r'^purchase/', PurchaseViewSet.as_view(), name='new purchase'),
]
