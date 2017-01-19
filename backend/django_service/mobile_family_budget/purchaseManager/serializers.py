from rest_framework import serializers

from purchaseManager.models import (
    PurchaseList,
    Purchase
)

from mobile_family_budget.utils.ulr_kwarg_consts import (
    GROUP_URL_KWARG,
    PURCHASE_LIST_URL_KWARG
)


class PurchaseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, required=True)
    count = serializers.IntegerField(min_value=1, required=False)
    price = serializers.FloatField(min_value=0, required=False)
    current_count = serializers.IntegerField(min_value=0, required=False)
    status = serializers.BooleanField(required=False)

    class Meta:
        model = Purchase
        fields = ('id', 'name', 'count', 'price', 'current_count', 'status')

    def create(self, validated_data):
        validated_data[PURCHASE_LIST_URL_KWARG] = self.context['view'].kwargs[PURCHASE_LIST_URL_KWARG]
        return Purchase.objects.create(**{k: v for k, v in validated_data.items() if v})


class PurchaseUpdateSerializer(PurchaseSerializer):
    name = serializers.CharField(max_length=30, required=False)

    def validate(self, data):
        if not data:
            raise serializers.ValidationError({'error': 'At least one field is required.'})
        return data

    def update(self, instance, validated_data):
        current_count = validated_data.get('current_count', instance.current_count)
        count = validated_data.get('count', instance.count)
        if current_count > count:
            raise serializers.ValidationError({'error': 'current count cannot be greater than common count'})
        if current_count == count:
            validated_data['status'] = True

        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.price = validated_data.get('price', instance.price)
        instance.current_count = current_count
        instance.count = count
        instance.save()

        return instance


class PurchaseListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)

    class Meta:
        model = PurchaseList
        fields = ('id', 'name')

    def create(self, validated_data):
        return PurchaseList.objects.create(budget_group_id=self.context['view'].kwargs[GROUP_URL_KWARG],
                                           name=validated_data['name'])
