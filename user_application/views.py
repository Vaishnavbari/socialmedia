from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import user_registration,post,like,comment
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import userSerializer,loginserializer,post_serialzer,comment_serializer
from rest_framework.authentication import *
from rest_framework.permissions import *
from .models import user_registration
from rest_framework import status
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .jwt_authorization import JWTAuthorization
from rest_framework.throttling import UserRateThrottle

from .custompagination import mypagination
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# def exceptionhandling(self,func):
#         def inner():
#             try:
#                 func()
#             except:
#                 return Response({"msg":"something went wrong"},status=500)
#         return inner 
class created_user(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(created_user, self).dispatch(request, *args, **kwargs)
    
   
    def post(self, request):
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
             if user_registration.objects.filter(username=serializer.validated_data.get("username")).exists():
                  return Response({"msg":"user already exist"},status=400)
             else :
                user = user_registration(first_name=serializer.validated_data.get("firstname"),last_name=serializer.validated_data.get("lastname"),username = serializer.validated_data.get("username"),password=make_password(serializer.validated_data.get("password")))
                user.save()
                token = get_tokens_for_user(user)
                return Response({"message": "Data saved successfully","token":token})
        return Response({"error": serializer.errors}, status=400)
    
    def get(self,request):
        return render(request,"user_application/register.html")
    
class login(APIView):
  
    def post(self,request):
       
        serializer=loginserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            if not username or not password:
                return Response({"meassage":"please provide username and password"})
            user = authenticate(request,username=username,password=password)

            if user is not None:
                 auth_login(request,user)
                 token=get_tokens_for_user(user)
                 return Response({"msg":"user login sucessfully","token":token})
            else:
                return Response("invalid login")
        else:
             return Response(serializer.errors)
        
    
    def get(self,request):
        return render(request,"user_application/login_page.html")

class update_user(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[JWTAuthorization]
        
    def put(self, request, id=None):
        if id is not None:
            
            user=user_registration.objects.filter(id=id).first()
            serializer = userSerializer(data=request.data,partial=True)  
            if serializer.is_valid():
                if user_registration.objects.filter(username=serializer.validated_data.get('username')):
                    return Response({"error":"username already exist"})
                else:
                    user.username = serializer.validated_data.get('username', user.username)
                    if serializer.validated_data.get('password') is not None: 
                        user.password = make_password(serializer.validated_data.get('password'))
                    else:
                        user.password=user.password  
                    user.first_name = serializer.validated_data.get('firstname',user.first_name)
                    user.last_name = serializer.validated_data.get('lastname',user.last_name)
                    user.last_login=serializer.validated_data.get('last_login',user.last_login)
                    user.is_superuser=serializer.validated_data.get('is_superuser',user.is_superuser)
                    user.email=serializer.validated_data.get('email,',user.email)
                    user.is_staff=serializer.validated_data.get('is_staff',user.is_staff)
                    user.is_active=serializer.validated_data.get('is_active',user.is_active)
                    user.date_joined=serializer.validated_data.get('date_joined',user.date_joined)
                    user.save()
                    return Response({"message": "Data updated successfully"}, status=201)
        return Response({"error": serializer.errors}, status=400)
    
# Post realated operartion 

# created post 

class created_post(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[JWTAuthorization]
    pagination_class = mypagination
    
    # @exceptionhandling
    def post(self,request,id=None):
        if request.user:
            serializer = post_serialzer(data=request.data)
            if serializer.is_valid():
                post.objects.create(image=serializer.validated_data.get("image"),user=request.user,caption=serializer.validated_data.get("caption")).save()
                return Response({"msg":"post created sucessfully"})
        return Response({"error": serializer.errors}, status=400)
            
    # @exceptionhandling     
    def get(self,request,id=None):
        post_list=post.objects.all()
        serializer = post_serialzer(post_list,many=True)
        return Response({"msg":serializer.data})
    
    # @exceptionhandling
    def delete(self, request, id ):
        if id is not None:
            if post.objects.filter(user=request.user.id):
                post_list=post.objects.filter(id=id).first()
                post_list.delete()
                return Response({"msg":"post deleted sucessfully"},status=200)
            else:
                return Response({"msg":"you are unauthorized user, you don't have permission to delete this post"},status=200)
        return Response({"msg":"something went wrong"},status=400)

class singlepost(APIView):

    # @exceptionhandling
    def get(self,request,pk):
        if pk is not None:
            post_list=post.objects.filter(id=pk).first()
            serializer = post_serialzer(post_list)
            return Response({"msg":serializer.data})
        return Response({"error": serializer.errors}, status=400)
      
# like related operation
class addlike(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[JWTAuthorization]
 
    # @exceptionhandling
    def post(self,request,id):
        if id is not None:
            post_list=post.objects.get(id=id)
            if request.user:
                like.objects.create(user=request.user,post_id=post_list)
                return Response({"msg":"like added sucessfully"})
        return Response({"msg":"something went wrong"},status=400)
    
    # @exceptionhandling
    def delete(self, request, id):
        if id is not None:
            if like.objects.filter(user=request.user):
                like.objects.filter(user=request.user).delete()
                return Response("like deleted sucessfully")
            else:
                return Response({"msg":"something went wrong"},status=200)
        return Response({"msg":"something went wrong"},status=400)
           

class addcomment(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [JWTAuthorization]
    
    # @exceptionhandling
    def post(self,request,id):
            if id is not None:
                post_list = post.objects.filter(id=id).first()
                if request.user:
                    serializer = comment_serializer(data=request.data)
                    if serializer.is_valid():
                        comment.objects.create(user=request.user,post_id=post_list,comments=serializer.validated_data.get("comments"))
                        return Response({"msg":"comment added sucessfully"},status=200)
            return Response({"msg":"something went wrong"},status=400)
    
    # @exceptionhandling
    def delete(self, request, id):
        if id is not None:
            if comment.objects.filter(user=request.user):
                comment.objects.filter(user=request.user).delete()
                return Response("comment deleted sucessfully")
        return Response({"msg":"something went wrong"},status=400)
            
