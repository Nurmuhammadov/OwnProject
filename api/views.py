from rest_framework.response import Response
from rest_framework.decorators import *
from .serializers import *
# from rest_framework.authentication import *
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import *
import random


@api_view(['POST'])
def sign_up(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    age = request.POST.get('age')
    usr = User.objects.create_user(username=username, password=password, email=email, age=age)
    profile = Profile.objects.create(user=usr)
    token, created = Token.objects.get_or_create(user=usr)
    return Response({'success': True, "Token": token.key})


@api_view(["POST"])
def log_in(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = User.objects.get(username=username)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'success': True, "Token": token.key})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def play(request):
    try:
        questions = Quiz.objects.all()
        quiz = []
        ser = []
        for i in questions:
            quiz.append(i)
        for j in range(5):
            r = random.choice(quiz)
            variants = Answer.objects.filter(quiz=r)
            dic_var = []
            for i in variants:
                dic_var.append({"id": i.id, "answer": i.answer})
            ser.append({"id": r.id,
                        "question": r.question,
                        "answer_is": r.answer,
                        "answer_count": r.answer_count,
                        "answer_given": r.answer_given,
                        "variants": dic_var})
            quiz.remove(r)
        print(ser)
        answers = Answer.objects.filter(quiz=1)
        return Response(ser)
    except Exception as err:
        print(err)
        return Response(f"{err}")


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_friend(request, pk):
    new_friend = User.objects.get(id=pk)
    if Friendship.objects.filter(friendship=new_friend):
        raise SystemError("Already friend")
    else:
        Friendship.objects.create(user=request.user, friendship=new_friend)
        return Response({'success': True})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def result_create(request):
    try:
        user_answered = request.POST['user_answered']
        true_answers = request.POST['true_answers']

        def convert(string):
            li = list(string.split(" "))
            return li

        true = 0
        false = 0
        for i, j in zip(convert(user_answered), convert(true_answers)):
            if i == j:
                true += 1
            else:
                false += 1
            print(i)

        Result.objects.create(profile=Profile.objects.get(user=request.user), solved_questions=true, field_questions=false)
        return Response({'success': True})
    except:
        return Response({'success': False})
