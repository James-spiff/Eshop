from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.contrib.auth.models import User
from base.serializers import ProductSerializer, UserSerializer, UserSerializerWithToken

#These is allows us to use JSON web tokens
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for key, value in serializer.items():    #loops through the UserSerializer response and get's all the data
            data[key] = value

        return data 

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {
            'detail': 'User with this email already exists'
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])  #set's the permissions i.e the type of user allowed to access this view
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data 
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  #set's the permissions i.e the type of user allowed to access this view
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):  #admin level view used to get all the users in the database
    users = User.objects.all()
    serializer = UserSerializer(users, many=True) #many=True is set to True because we are expecting more than one data in the case of only one data it's set to False
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):  #admin level view used to get all the users in the database
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False) #many=True is set to True because we are expecting more than one data in the case of only one data it's set to False
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAdminUser])  
def updateUser(request, pk):
    user = User.objects.get(id=pk)

    data = request.data 
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.is_staff = data['isAdmin']

    user.save()
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)



@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')