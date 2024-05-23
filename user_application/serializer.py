from rest_framework import serializers 
from user_application.models import user_registration
from rest_framework.response import Response
class userSerializer(serializers.Serializer):
    username = serializers.CharField(allow_null=True, required=False)
    firstname = serializers.CharField(allow_blank=True,allow_null=True)
    lastname = serializers.CharField(allow_blank=True,allow_null=True)
    password = serializers.CharField(max_length=128, required=False)
    last_login = serializers.DateTimeField(allow_null=True, required=False)
    is_superuser = serializers.BooleanField(allow_null=True, required=False)
    email = serializers.EmailField(allow_blank=True,required=False)
    is_staff = serializers.BooleanField(allow_null=True, required=False)
    is_active = serializers.BooleanField(allow_null=True, required=False)
    date_joined = serializers.DateTimeField(allow_null=True, required=False)

class loginserializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
   


class post_serialzer(serializers.Serializer):
    image=serializers.ImageField()
    caption=serializers.CharField()


class comment_serializer(serializers.Serializer):
    comments=serializers.CharField()