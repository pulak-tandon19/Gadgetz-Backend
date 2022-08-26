from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from base.models import *
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views import View
from django.contrib.auth.hashers import make_password
from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        serializer= UserSerializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k]=v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class getUserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,*args,**kwargs):
        user=self.request.user
        serializer= UserSerializer(user, many=False)
        return Response(serializer.data)

class updateUserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,*args,**kwargs):
        user=self.request.user
        serializer= UserSerializerWithToken(user, many=False)
        data = self.request.data
        user.first_name= data['name']
        user.username= data['email']
        user.email= data['email']

        if data['password']!='':
            user.password= make_password(data['password'])
        
        user.save()

        return Response(serializer.data)

class registerUser(APIView):
    def post(self, *args, **kwargs):
        data = self.request.data

        try:
            user = User.objects.create(
            first_name = data['name'],
            username= data['email'],
            email  = data['email'],
            password= make_password(data['password'])
         )
        except:
            message={'detail': 'User with this email already exists.'}
            return Response(message, status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializerWithToken(user, many= False)
        return Response(serializer.data)

class getUsers(APIView):
    permission_classes = (IsAdminUser,)
    def get(request, self):
        users= User.objects.all()
        serializer= UserSerializer(users, many=True)
        return Response(serializer.data)

class getUserById(APIView):
    permission_classes = (IsAdminUser,)
    def get(request, self, pk):
        user= User.objects.get(id=pk)
        serializer= UserSerializer(user, many=False)
        return Response(serializer.data)

class updateUser(APIView):
    permission_classes = (IsAdminUser,)
    def put(self, request, pk,*args,**kwargs):
        user=User.objects.get(id=pk)
        data = self.request.data
        user.first_name= data['name']
        user.username= data['email']
        user.email= data['email']
        user.is_staff= data['isAdmin']
        user.save()

        serializer= UserSerializer(user, many=False)
        return Response(serializer.data)

class DeleteUser(APIView):
    permission_classes = (IsAdminUser,)
    def delete(self, request, pk):
        user= User.objects.get(id=pk)
        user.delete()
        return Response('User is  deleted!')
