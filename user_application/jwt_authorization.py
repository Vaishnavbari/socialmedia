# From rest_framework 
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
import jwt
from django.conf import settings
from .models import user_registration, expire_token_check,access_token
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


class JWTAuthorization(permissions.BasePermission):

    @staticmethod
    def decode_jwt_token(token):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return decoded_token
        except:
            return None
    
    
    def authenticate(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                return None

            token = auth_header.split(' ')[-1]

            if access_token.objects.filter(token=token).exists():
                            
                decoded_token = self.decode_jwt_token(token)

                if decoded_token:
                    user_id = decoded_token['user_id']
                    try:
                        user = user_registration.objects.filter(id=user_id).first()

                        return user
                    except user_registration.DoesNotExist:
                        return None
                return None
            else :
                return None
        except Exception as e:
            raise AuthenticationFailed(f"Token verification failed: {str(e)}")
        

    def has_permission(self, request, view):
        user = self.authenticate(request)
        request.user = user  # Set the authenticated user in the request
        
        return user is not None
    


