from django.shortcuts import render
#from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.contrib.auth.models import User
from .models import Product
from .serializers import ProductSerializer, UserSerializer, UserSerializerWithToken

#These is allows us to use JSON web tokens
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status

 
#from .products import products


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     #add custom claims
    #     token['username'] = user.username
    #     token['message'] = 'hello world'

    #     return token 

    # The commented out code let's us customize our JWT response adding fields like username and the message

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
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True) #many=True is set to True because we are expecting more than one data in the case of only one data it's set to False
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
        
    return Response(serializer.data)