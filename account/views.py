from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from account.serielizers import StudentSerializer,LoginSerializer
from account.models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions,viewsets,generics
from rest_framework.views import APIView,status
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

# Create your views here.
class StudentRegister(generics.GenericAPIView):
    serializer_class=StudentSerializer

    def post(self,request,*args,**kwargs):
        serializer=StudentSerializer(data=request.data)
        #print(serializer)
        if serializer.is_valid(raise_exception=True):
            #print(serializer['password'])

            user=serializer.newsave()
            return Response("done")
        else:
            return Response('not done')



class Login(generics.GenericAPIView):
    serializer_class=LoginSerializer

    def post(self,request,*args,**kwargs):
        #serializer=self.get_serializer(data=request.data)
        #user=authenticate(request,email=serializer.email,password=serializer.password)
        email = request.data.get("email")
        password = request.data.get("password")
        print(email,password)
        #print(serializer.email)
        user = authenticate(email=email,password=password)
        print(user)
        if user is not None:


            login(request, user)

            data = {
                "Name": user.first_name + " " + user.last_name,
                "id": user.pk,
                "Username": user.username,
                "Message":"done"
            }


            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {"Message": "There was error authenticating"}
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
