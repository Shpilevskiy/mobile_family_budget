from rest_framework.response import Response
from rest_framework import (
    generics,
    permissions,
    status
)

from account.permissions import IsGroupMember

from mobile_family_budget.utils.ulr_kwarg_consts import (
    GROUP_URL_KWARG,
    PURCHASE_LIST_URL_KWARG,
    PURCHASE_URL_KWARG
)

from purchaseManager.models import (
    Purchase,
    PurchaseList
)
from purchaseManager.serializers import (
    PurchaseSerializer,
    PurchaseListSerializer,
    PurchaseUpdateSerializer
)


class PurchasesListsListCreateApiView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    serializer_class = PurchaseListSerializer

    def get_queryset(self):
        return PurchaseList.objects.participant(self.kwargs[GROUP_URL_KWARG])


class PurchaseListRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    serializer_class = PurchaseListSerializer
    lookup_url_kwarg = PURCHASE_LIST_URL_KWARG

    def get_queryset(self):
        return PurchaseList.objects.participant(self.kwargs[GROUP_URL_KWARG],
                                                self.kwargs[PURCHASE_LIST_URL_KWARG])


class PurchasesListCreateApiView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return Purchase.objects.participant(self.kwargs[PURCHASE_LIST_URL_KWARG])

    def get(self, request, *args, **kwargs):
        if PurchaseList.objects.filter(id=kwargs[PURCHASE_LIST_URL_KWARG]).exists():
            return super().get(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Purchases list is not found."})

    def post(self, request, *args, **kwargs):
        if PurchaseList.objects.filter(id=kwargs[PURCHASE_LIST_URL_KWARG]).exists():
            return super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Purchases list is not found."})


class PurchaseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    serializer_class = PurchaseUpdateSerializer
    lookup_url_kwarg = PURCHASE_URL_KWARG

    def get_queryset(self):
        return Purchase.objects.participant(
            self.kwargs[PURCHASE_LIST_URL_KWARG],
            self.kwargs[PURCHASE_URL_KWARG])
