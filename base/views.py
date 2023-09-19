from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from .permissions import CustomModelPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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
        return Response({'token':token.key})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register(request):
    password = request.data.get('password')
    group_id = request.data.get('group')
    try:
        group_object = Group.objects.get(id=group_id)
    except:
        return Response({'error':'No such groups!'})
    hash_password = make_password(password)
    request.data['password'] = hash_password
    request.data['company_info'] = request.user.company_info.id
    serializer = UserInfoSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.groups.add(group_object.id)
        user.save()
        return Response({'data':'User created!'})
    else:
        return Response({'error':serializer.errors})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def admin_create(request):
    password = request.data.get('password')
    try:
        group_object = Group.objects.get(name='Admin')
    except:
        return Response({'error':'No such groups!'})
    hash_password = make_password(password)
    request.data['password'] = hash_password
    serializer = UserInfoSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.groups.add(group_object.id)
        user.save()
        return Response({'data':'Admin created!'})
    else:
        return Response({'error':serializer.errors})

class CompanyInfoApiView(GenericAPIView):
    queryset_model = CompanyInfo
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # filterset_fields = ['address']
    search_fields = ['address','name']
    permission_classes = [IsAuthenticated,CustomModelPermission]

    def get(self,request):
        company_info_objects = self.get_queryset()
        filter_objects = self.filter_queryset(company_info_objects)
        serializer = CompanyInfoSerializer(filter_objects,many=True)
        return Response({'data':serializer.data})
    
    def post(self,request):
        serializer = CompanyInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'Data created!'})
        else:
            return Response({'error':serializer.errors})
        
class CompanyInfoIdApiView(GenericAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAuthenticated,CustomModelPermission]

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

class GroupApiView(GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self,request):
        group_objects = self.get_queryset()
        serializer = self.serializer_class(group_objects,many=True)
        return Response({'data':serializer.data})