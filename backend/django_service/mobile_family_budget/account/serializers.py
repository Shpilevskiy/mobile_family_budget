from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import RefLink
from .models import BudgetGroup
from rest_framework import serializers


class BudgetGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class RefLinkSerializer(serializers.ModelSerializer):
    expire_date = serializers.DateField()
    activation_count = serializers.IntegerField(min_value=0)

    class Meta:
        model = RefLink
        fields = ('link',
                  'creation_date',
                  'expire_date',
                  'activation_count',)
        read_only_fields = ('creation_date', 'link')

    def update(self, instance, validated_data):
        instance.expire_date = validated_data.get('expire_date', instance.expire_date)
        instance.activation_count = validated_data.get('activation_count', instance.activation_count)
        instance.save()
        return instance


class BudgetGroupSerializer(serializers.HyperlinkedModelSerializer):
    group_owner = BudgetGroupUserSerializer()

    class Meta:
        model = BudgetGroup
        fields = ('id', 'name', 'group_owner')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(allow_blank=True, required=False, default='')
    first_name = serializers.CharField(allow_blank=True, required=False, default='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name']
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class BudgetGroupCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=120)

    class Meta:
        model = BudgetGroup
        fields = ('name',)

    def create(self, validated_data):
        budget_group = BudgetGroup(
            group_owner=validated_data['owner'],
            name=validated_data['name']
        )
        budget_group.save()
        return budget_group


class AddUserToGroupSerializer(serializers.ModelSerializer):
    link = serializers.CharField(min_length=1, max_length=80)

    class Meta:
        model = RefLink
        fields = ('link',)
