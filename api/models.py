from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question = models.CharField(max_length=20)
    answer_count = models.IntegerField(default=3)
    answer_given = models.IntegerField(default=0)


class Answer(models.Model):
    answer = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class User(User):
    age = models.IntegerField()