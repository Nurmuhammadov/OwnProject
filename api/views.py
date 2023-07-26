from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import *


class SignUp(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        try:
            username = request.data['username']
            passwd = request.data['password']
            age = request.data['age']
            email = request['email']
            emails = False
            for i in self.queryset:
                if i.email == email:
                    emails = True
                    break
            print(emails)
            user_create = User.objects.create_user(username=username, email=email, password=passwd, age=age)
            return Response({'success': True})
        except:
            return Response({'success': False})

class Login(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = ([JWTAuthentication])
    permission_classes = ([IsAuthenticated])

    def sign_up(self, request):
        try:
            username = request.data['username']
            passwd = request.data['password']

            user = authenticate(username=username, password=passwd)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'token': token.key,
                }
                return Response(data)
            else:
                return Response({'message': 'No such user!'})
            return Response({'success': False})
        except:
            return Response({'success': True})