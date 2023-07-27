from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import *


@api_view(['POST'])
def sign_up(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    age = request.POST.get('age')
    User.objects.create_user(username=username, password=password, email=email, age=age)
    token, created = Token.objects.get_or_create(user=username)
    return Response({'success': True, "Token": token.key})