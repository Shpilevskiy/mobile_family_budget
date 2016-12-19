from rest_framework import serializers


class PurchaseListSerializer(serializers.Serializer):
    name = serializers.CharField()


class PurchaseSerializer(serializers.Serializer):
    name = serializers.CharField()
    count = serializers.IntegerField()
    price = serializers.FloatField()
    current_count = serializers.IntegerField()
    status = serializers.BooleanField()
