# from django 
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import user_registration,post,like,comment,access_token
from django.contrib.auth import login , logout
from django.contrib.auth.hashers import make_password
from .jwt_authorization import JWTAuthorization
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.template.loader import render_to_string

# from rest framework 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import *
from rest_framework.permissions import *
from rest_framework_simplejwt.tokens import RefreshToken

# Import created serializer  and pagination 
from .serializer import userSerializer,loginserializer,post_serialzer,comment_serializer,emailserializer, passwordserializer
from .custompagination import mypagination

# others 
from functools import wraps
from django.views.decorators.csrf import csrf_exempt


def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def exceptionhandling(func):

    @wraps(func)
    def inner(*args, **kwargs):

        try:

            return func(*args, **kwargs)
        
        except Exception as e:

            return Response({"msg": "something went wrong", "error": str(e)}, status=500)
        
    return inner


class created_user(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(created_user, self).dispatch(request, *args, **kwargs)
    
    @exceptionhandling
    def post(self, request):
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
             if user_registration.objects.filter(username=serializer.validated_data.get("username")).exists():
                  return Response({"message":"user already exist"},status=status.HTTP_400_BAD_REQUEST)
             else :
                user = user_registration(first_name=serializer.validated_data.get("firstname"), last_name=serializer.validated_data.get("lastname"), username = serializer.validated_data.get("username"), password=make_password(serializer.validated_data.get("password")))
                user.save()
                token = get_tokens_for_user(user)
                return Response({"message": "Data saved successfully", "token":token, "user_data":serializer.data})
        else:    
             return Response({"error": serializer.errors}, status=400)
    
    @exceptionhandling
    def get(self,request):
        return render(request,"user_application/register.html")
    

class userlogin(APIView):
   
    @exceptionhandling
    def post(self,request):

        serializer=loginserializer(data=request.data)

        if serializer.is_valid(raise_exception=True):

            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            if not username or not password:
                return Response({"message":"Please provide username and password"})
            
            user = authenticate(request,username=username,password=password)

            if user is not None:
                 login(request,user)
                 token=get_tokens_for_user(user)
                 access_token.objects.create(token=token.get("access"))
                 return Response({"message":"User login sucessfully", "token":token, "user_data":serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"invalid login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
             return Response(serializer.errors)
        
    @exceptionhandling
    def get(self,request):
        return render(request,"user_application/login_page.html")


class update_user(APIView):

    permission_classes=[JWTAuthorization]

    @exceptionhandling 
    def put(self, request, id=None):

        if id is not None:

            user=user_registration.objects.filter(id=id).first()
            serializer = userSerializer(data=request.data,partial=True) 

            if request.user == user:
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
                        user.last_login = serializer.validated_data.get('last_login',user.last_login)
                        user.is_superuser = serializer.validated_data.get('is_superuser',user.is_superuser)
                        user.email = serializer.validated_data.get('email,',user.email)
                        user.is_staff = serializer.validated_data.get('is_staff',user.is_staff)
                        user.is_active = serializer.validated_data.get('is_active',user.is_active)
                        user.date_joined = serializer.validated_data.get('date_joined',user.date_joined)
                        user.save()
                        return Response({"message": "Data updated successfully","user_data":serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else :
                return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


# Post realated operartion 
# created post 
class created_post(APIView):

    permission_classes=[JWTAuthorization]
    pagination_class = mypagination
    
    @exceptionhandling
    def post(self,request,id=None):
        if request.user:
            serializer = post_serialzer(data=request.data)
            if serializer.is_valid():
                post_data=post.objects.create(image=serializer.validated_data.get("image"),user=request.user,caption=serializer.validated_data.get("caption"),title=serializer.validated_data.get("title"))

                return Response({"message":"post created sucessfully","post_data": post_serialzer(post_data).data},status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
            
    
class singlepost(APIView):
    
    permission_classes=[JWTAuthorization]

    @exceptionhandling     
    def get(self,request,pk=None):
        if pk is not None:
            post_list=post.objects.filter(id=pk).first()
            serializer = post_serialzer(post_list)
            return Response({"message":serializer.data},status=status.HTTP_200_OK)
        else:
            post_list=post.objects.all()
            serializer = post_serialzer(post_list,many=True)
            return Response({"message":serializer.data},status=status.HTTP_200_OK)
        
    @exceptionhandling
    def delete(self, request, pk):
        if pk is not None:
            post_data=post.objects.filter(id=pk,user=request.user.id).first()
            if post_data:
                post_data.delete()
                return Response({"message":"post deleted sucessfully"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"you are unauthorized user, you don't have permission to delete this post"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
    
    @exceptionhandling
    def put(self, request , pk):
         post_data = post.objects.filter(id=pk,user=request.user.id).first()
         if post_data :
             serializer=post_serialzer(data=request.data, partial=True)
             if serializer.is_valid():
                 post_data.title = serializer.validated_data.get("title", post_data.title)
                 post_data.image = serializer.validated_data.get("image", post_data.image)
                 post_data.caption = serializer.validated_data.get("caption", post_data.caption)
                 post_data.save()
                 return Response({"message":"Your post updated sucessfully","post_data":serializer.data}, status=status.HTTP_200_OK)
             else:
                 return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
         else:
             return Response({"message":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
# like related operation
class addlike(APIView):

    permission_classes=[JWTAuthorization]
 
    @exceptionhandling
    def post(self,request,id):
        post_id=post.objects.filter(id=id).first()
        if post_id :
            post_list=like.objects.filter(post_id=post_id.id,user=request.user.id).first()
        else:
            return Response({"message":"something went wrong"},status=status.HTTP_404_NOT_FOUND)
        if not post_list :
            like.objects.create(user=request.user,post_id=post_id)
            return Response({"message":"like added sucessfully"},status=status.HTTP_200_OK)
        else:  
            post_list.delete()
            return Response({"message":"like deleted sucessfully"},status=status.HTTP_200_OK)
    

class addcomment(APIView):

    permission_classes = [JWTAuthorization]
    
    @exceptionhandling
    def post(self,request,id):
        post_list = post.objects.filter(id=id).first()
        if post_list :
            serializer = comment_serializer(data=request.data)
            if serializer.is_valid() :
                comment.objects.create(user=request.user,post_id=post_list,comments=serializer.validated_data.get("comments"))
                return Response({"message":"comment added sucessfully","comment":serializer.data },status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
    
    @exceptionhandling
    def delete(self, request, id):
        comment_id = comment.objects.filter(id=id).first()
        if comment_id :
            comment_user = comment.objects.filter(id=comment_id.id, post_id=comment_id.post_id, user=request.user.id).first()
            if comment_user:
                comment_user.delete()
                return Response({"message":"comment deleted sucessfully"},status=status.HTTP_200_OK)
            else:
                return Response({"message":"you are unauthorized user, you don't have permission to delete this comment"},status=status.HTTP_404_NOT_FOUND)
        else :        
            return Response({"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
            
    @exceptionhandling
    def put(self, request, id):
        comment_id= comment.objects.filter(id=id).first()
        if comment_id :
            comment_user = comment.objects.filter(id=comment_id.id).first()
            if comment_user:
                serializer = comment_serializer(data=request.data, partial=True)
                if serializer.is_valid():
                    comment_user.comments=serializer.validated_data.get("comments",comment_user.comments)
                    comment_user.save()
                    return Response({"message": "Your comment updated sucessfully"}, status=status.HTTP_200_OK)
                else: 
                    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"you are unauthorized user, you don't have permission to edit this comment"},status=status.HTTP_404_NOT_FOUND)
        else : 
            return Response({"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class Logout_user(APIView):
    
    permission_classes = [JWTAuthorization]

    @exceptionhandling
    def get(self,request):
            
            if request.user :

                auth_header = request.headers.get('Authorization')
                
                if not auth_header:

                    return Response({'error': 'Authorization header missing'}, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                      token = auth_header.split(" ")[1]

                except IndexError:
                    return Response({'error': 'Token format invalid'}, status=status.HTTP_400_BAD_REQUEST) 

                check_token = access_token.objects.filter(token=token)

                if check_token.exists():
                    check_token.delete()

                logout(request)

                return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
                
            else:
                return Response({'error': 'Somthing went wrong '}, status=status.HTTP_404_NOT_FOUND)

    
class forgot_password(APIView):

    permission_classes = [JWTAuthorization]
     
    def post(self,request):
        serializer=emailserializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data.get("email")
            if user_registration.objects.filter(email=email).exists():
                if request.user.email == serializer.validated_data.get("email"):
                 
                    token = default_token_generator.make_token(request.user)
                    uid = urlsafe_base64_encode(force_bytes(request.user.id))
                    password_reset_url = f"http://127.0.0.1:8000/password_request_confirm/{uid}/{token}"
                
                    email_subject = 'Password Reset Request'
                    email_body = render_to_string('user/password_reset_email.txt', {
                        'user': request.user,
                        'password_reset_url': password_reset_url,
                    })

                    send_mail(email_subject, email_body, request.user.email, [request.user.email])
                    return Response({"message": "Password reset link send sucessfully"}, status=status.HTTP_200_OK)
                
                else:
                    return Response({"message":"you are unauthorized user"},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message":"email is not valid"},status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class password_confirm_mail(APIView) :

    def post(self,request, uidb64, token) :
        
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_registration.objects.filter(id=uid).first()

        if user and default_token_generator.check_token(user, token) :

            serializer = passwordserializer(data=request.data)

            if serializer.is_valid() :
              password = serializer.validated_data.get("password")
              if password :
                user.password = make_password(password)
                user.save()
                return Response({"message":"Password reset sucessfully"}, status=status.HTTP_200_OK)
              else :
                return Response({"message":"Please provide the password"}, status=status.HTTP_404_NOT_FOUND)
            else :
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else :
            return Response({"message":'Invalid password reset link.'}, status=status.HTTP_200_OK)