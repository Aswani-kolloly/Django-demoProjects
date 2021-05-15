from rest_framework.serializers import ModelSerializer
from .models import User, AccountDetails, TransactionHistory
from rest_framework import serializers


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class BankAccountModelSerializer(ModelSerializer):
    class Meta:
        model = AccountDetails
        fields = ['account_num', 'user_name', 'balance', 'acnt_type']


class TransactionSerializer(serializers.Serializer):
    # account_num=BankAccountModelSerializer()
    account_num = serializers.CharField()
    to_acno = serializers.IntegerField()
    amount = serializers.IntegerField()
    date = serializers.DateField(required=False)

    def create(self, validated_data):
        acno = validated_data["account_num"]
        acnt_obj = AccountDetails.objects.get(account_num=acno)
        validated_data["account_num"] = acnt_obj
        return TransactionHistory.objects.create(**validated_data)


class WithdrawSerializer(serializers.Serializer):
    amount = serializers.IntegerField()


class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
# class TransactionSerializer(serializers.Serializer):
