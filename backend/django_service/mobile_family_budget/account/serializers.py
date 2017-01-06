from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import RefLink
from .models import BudgetGroup
from rest_framework import serializers


class GroupUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', )


# class GroupUserSerializer(serializers.Serializer):
#     username = serializers.CharField()


class RefLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RefLink
        fields = ('link',
                  'creation_date',
                  'expire_date',
                  'activation_count',)
        read_only_fields = ('creation_date', 'link')


# class BudgetGroupUsersSerializers(serializers.ListSerializer):
#     users = UserSerializer(read_only=True, many=True)
    #
    # class Meta:
    #     model=BudgetGroup
    #     fields = ('users',)


class BudgetGroupSerializer(serializers.HyperlinkedModelSerializer):
    group_owner = GroupUserSerializer()
    users = GroupUserSerializer(read_only=True, many=True)
    invite_link = RefLinkSerializer()

    class Meta:
        model = BudgetGroup
        fields = ('name', 'login', 'group_owner', 'users', 'invite_link')

    # def create(self, validated_data):
    #     # budget_group = BudgetGroup(
    #     #     name=validated_data['name'],
    #     #     login=validated_data['login'],
    #     #     users=validated_data['users'],
    #     # )


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'groups', )
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


class BudgetGroupCreateSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=120)

    class Meta:
        model = BudgetGroup
        fields = ('name', )
