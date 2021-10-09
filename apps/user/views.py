from django.shortcuts import render

# Create your views here.

# 设计视图时，可以从功能考虑需要继承那个View
# 注册 只需要 post即可。所以继承 CreateAPIView 提供了post

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from user.serializer import RegisterSerializer


class RegisterView(CreateAPIView):
    # 因为只是查询 所以只需要指定查询集即可。
    serializer_class = RegisterSerializer


class UsernameValidateView(APIView):
    """
    校验用户名是否重复
    """
    def get(self, request,username):
        data_dict={
            'username': username,
            'count': User.objects.filter(username=username).count()
        }
        return Response(data_dict)


class EmailValidateView(APIView):

    """
    有限格式校验
    """
    def get(self,request,email):
        data_dict = {
            "eamil": email,
            "count": User.objects.filter(email=email).count()
        }
        return Response(data_dict)