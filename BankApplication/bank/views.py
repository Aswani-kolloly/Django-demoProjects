from django.shortcuts import render
import sys
from rest_framework.views import APIView
from .serializers import UserModelSerializer, LoginSerializer, BankAccountModelSerializer, WithdrawSerializer, \
    DepositSerializer, TransactionSerializer
from rest_framework import mixins, generics, status, permissions
from django.contrib.auth import login, logout, authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import AccountDetails, TransactionHistory, User
from django.http import HttpResponse


# Create your views here.
#checks whether account no is invalid or not
def check(acno):
    try:
        ob = AccountDetails.objects.get(account_num=acno)
        return ob
    except Exception as e:
        return None

class UserDetailsMixin(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = UserModelSerializer

    def post(self, request):
        return self.create(request)


class UserLogin(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            uname = serializer.validated_data.get("username")
            pswd = serializer.validated_data.get("password")
            user = User.objects.get(username=uname)
            # user = authenticate(request, username=uname, password=pswd)
            # print(pswd)
            if (user.username == uname) & (user.password == pswd):
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=204)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)


class BankAccountApi(generics.GenericAPIView, mixins.CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BankAccountModelSerializer

    def get(self, request):
        acnt = AccountDetails.objects.last()
        if acnt:
            acno = acnt.account_num + 1
        else:
            acno = 1000
        return Response({"acno": acno})

    def post(self, request):
        return self.create(request)


class BalanceApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_num):
        acnt_obj = check(account_num)
        if acnt_obj is not None :
            serializer = BankAccountModelSerializer(acnt_obj)
            return Response(serializer.data)
        else:
            return Response({"Warning: Invalid acno, "+str(account_num)})


class WithdrawApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, account_num):
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            acnt_obj = check(account_num)
            if acnt_obj is not None:
                amt = serializer.validated_data.get("amount")
                if amt <= (acnt_obj.balance-1000):#min bal:1000
                    acnt_obj.balance -= amt
                    acnt_obj.save()
                    return Response({"msg": "amt deducted, Balance amount is " + str(acnt_obj.balance)})
                else:
                    return Response({"msg": "no sufficient blnce"})
            else:
                return Response({"Warning " + str(account_num) + " doesn't exist"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, account_num):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            acnt_obj = check(account_num)
            if acnt_obj is not None:
                amt = serializer.validated_data.get("amount")
                acnt_obj.balance += amt
                acnt_obj.save()
                return Response({"msg": "amt added Current balance is " + str(acnt_obj.balance)})
            else:
                return Response({"Warning " + str(account_num) + " doesn't exist"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionApi(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, account_num):
        acnt_obj=check(account_num)
        if acnt_obj is not None:
            qset_debit_transactions = TransactionHistory.objects.filter(account_num=acnt_obj)
            print(qset_debit_transactions)# fetching all debit transactions
            qset_credit_transactions = TransactionHistory.objects.filter(to_acno=account_num)# fetching credit transactions
            serializer1 = TransactionSerializer(qset_debit_transactions, many=True)
            serializer2 = TransactionSerializer(qset_credit_transactions, many=True)
            return Response({"All Debit Transactions": serializer1.data ,"All credit transactions":serializer2.data },status=status.HTTP_200_OK)
        else:
            return Response({"Warning": "Account num "+str(account_num)+" doesn't exist"})

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            from_acno = serializer.validated_data.get("account_num")
            to_acno = serializer.validated_data.get("to_acno")
            amt = serializer.validated_data.get("amount")
            from_acnt_obj = check(from_acno)
            to_acnt_obj = check(to_acno)
            if from_acnt_obj is not None and to_acnt_obj is not None:
                if amt <= (from_acnt_obj.balance-1000):
                    serializer.save()
                    from_acnt_obj.balance-=amt
                    to_acnt_obj.balance+=amt
                    from_acnt_obj.save()
                    to_acnt_obj.save()
                    return Response({"msg": str(amt) + "has been sent to acno: " + str(to_acno)})
                else:
                    return Response({"No Sufficient balance"})
            elif from_acnt_obj is None:
                return Response({"Warning ":"invalid account no "+str(from_acno)})
            elif to_acnt_obj is None:
                return Response({"Warning ": "invalid account no " + str(to_acno)})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApi(APIView):
    def get(self, request):
        logout(request)
        return Response({"msg": "user logged out"})
        # request.user.auth_token.delete()
