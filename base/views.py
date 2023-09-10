from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.
# @api_view(['GET'])
# def companyInfoApiView(request):
#     company_info_objects = CompanyInfo.objects.all()
#     serializer = CompanyInfoSerializer(company_info_objects,many=True)
#     return Response(serializer.data)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email,password=password)
    if user == None:
        return Response('User not found!')
    else:
        token,_ = Token.objects.get_or_create(user=user)
        return Response(token.key)


class CompanyInfoApiView(GenericAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request):
        company_info_objects = self.get_queryset()
        serializer = CompanyInfoSerializer(company_info_objects,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = CompanyInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data created!')
        else:
            return Response(serializer.errors)
        
class CompanyInfoIdApiView(GenericAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            company_info_object = CompanyInfo.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = CompanyInfoSerializer(company_info_object)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            company_info_object = CompanyInfo.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = CompanyInfoSerializer(company_info_object,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data updated successfully')
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        try:
            company_info_object = CompanyInfo.objects.get(id=pk)
        except:
            return Response('Data not found!')
        company_info_object.delete()
        return Response('Data deleted successfully!')
