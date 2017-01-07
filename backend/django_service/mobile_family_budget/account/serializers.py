from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import RefLink
from .models import BudgetGroup
from rest_framework import serializers


class BudgetGroupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class RefLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RefLink
        fields = ('link',
                  'creation_date',
                  'expire_date',
                  'activation_count',)
        read_only_fields = ('creation_date', 'link')


class BudgetGroupSerializer(serializers.HyperlinkedModelSerializer):
    group_owner = BudgetGroupUserSerializer()
    invite_link = RefLinkSerializer()

    class Meta:
        model = BudgetGroup
        fields = ('id', 'name', 'group_owner', 'invite_link')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
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
    class Meta:
        model = RefLink
        fields = ('link',)

        validators = [
            UniqueTogetherValidator(
                queryset=RefLink.objects.all(),
                fields=('link',)
            )
        ]