from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

#加载静态界面index首页


class IndexApiView(APIView):

    def get(self,request):
        return Response(template_name='index.html')
