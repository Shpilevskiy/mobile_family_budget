from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import BudgetGroup
from .models import RefLink
from rest_framework import serializers


class GroupUserSerializer(serializers.Serializer):
    username = serializers.CharField()



class BudgetGroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    login = serializers.CharField()
    group_owner = GroupUserSerializer()
    users = GroupUserSerializer(read_only=True, many=True)



class RefLinkSerializer(serializers.HyperlinkedModelSerializer):
    budget_group = BudgetGroupSerializer(read_only=True)

    class Meta:
        model = RefLink
        fields = ('link',
                  'creation_date',
                  'expire_date',
                  'activation_count',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    budget_group = BudgetGroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'groups', 'budget_group', 'invite_link')
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


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
