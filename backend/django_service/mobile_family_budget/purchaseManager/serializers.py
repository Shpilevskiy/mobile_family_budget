from rest_framework import serializers

from purchaseManager.models import PurchaseList

from mobile_family_budget.utils.ulr_kwarg_consts import GROUP_URL_KWARG


class PurchaseListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)

    class Meta:
        model = PurchaseList
        fields = ('id', 'name')

    def create(self, validated_data):
        purchase_list = PurchaseList(budget_group_id=self.context['view'].kwargs[GROUP_URL_KWARG],
                                     name=validated_data['name'])
        purchase_list.save()
        return purchase_list


class PurchaseSerializer(serializers.Serializer):
    name = serializers.CharField()
    count = serializers.IntegerField()
    price = serializers.FloatField()
    current_count = serializers.IntegerField()
    status = serializers.BooleanField()
    id = serializers.IntegerField()
