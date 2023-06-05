import datetime, jwt

from rest_framework.authentication import BaseAuthentication


from rest_framework import status,exceptions
from list_api.models import CustomUser

from rest_framework.authentication import get_authorization_header
import os 

def create_access_token(id):

    return jwt.encode({
        'user_id':id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300000), 
        'iat': datetime.datetime.utcnow(), 
    }, os.environ.get("ACCESS_TOKEN_SECRET"), algorithm='HS256')

def create_refresh_token(id):
    return jwt.encode({
        'user_id':id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7), 
        'iat': datetime.datetime.utcnow(), 
    }, os.environ.get("REFRESH_TOKEN_SECRET"), algorithm='HS256')


def decode_access_token(token):
    try:
        payload = jwt.decode(token, os.environ.get("ACCESS_TOKEN_SECRET") , algorithms='HS256')
        return payload['user_id']
    except Exception as e:
        print(e)
        raise exceptions.AuthenticationFailed('unauthenticated')


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token,os.environ.get("REFRESH_TOKEN_SECRET"), algorithms='HS256')
        return payload['user_id']
    except Exception as e:
        print(e)
        raise exceptions.AuthenticationFailed('unauthenticated')


class JWTAuthentication(BaseAuthentication):
     def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            user_id = decode_access_token(token)

            user = CustomUser.objects.get(pk=user_id)
    
            return (user, None)
        raise exceptions.AuthenticationFailed('unauthenticated')     

  
            
          