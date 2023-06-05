from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from list_api.serializers.user_serializer import UserSerializer
from list_api.models import CustomUser, UserToken
import datetime



 

from list_api.authentication import create_access_token, create_refresh_token, JWTAuthentication, decode_refresh_token

class SignUp(APIView):
    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Password do not match to confirm-password')
        
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = serializer.data
        print("user: " , user)
        access_token = create_access_token(user["id"])
        refresh_token = create_refresh_token(user["id"])


        UserToken.objects.create(user_id=user["id"],
                                  token=refresh_token,
                                  expired_at= datetime.datetime.utcnow() + datetime.timedelta(days=7))


        response = Response()

        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

        response.data = {
            'token': access_token
        }
        
        return response

class Login(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']

        user =  CustomUser.objects.filter(username=username).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid credentials')
        
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)


        UserToken.objects.create(user_id=user.id,
                                  token=refresh_token,
                                  expired_at= datetime.datetime.utcnow() + datetime.timedelta(days=7))

        response = Response()

        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

        response.data = {
            'token': access_token
        }
        
        return response

class GetUser(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        data = serializer.data
        return Response(data)


class RefreshToken(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        if not UserToken.objects.filter(user_id=id,
                                        token=refresh_token,
                                        expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)
                                        ).exists():
            raise exceptions.AuthenticationFailed('unauthenticated')     

        new_access_token = create_access_token(id)
        return Response({
            'token': new_access_token
        })

class Logout(APIView):
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')

        UserToken.objects.filter(token=refresh_token).delete()

        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message': 'cookie deleted successfully'
        }

        return response


# class ForgotPassword(APIView):
#     def post(self,request):
#         token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

#         Reset.objects.create(
#             username=request.data['username'],
#             token=token
#         )

#         return Response({
#             'message': 'success'
#         })

# class ResetPassword(APIView):
#     def post(self,request):
#         data = request.data





