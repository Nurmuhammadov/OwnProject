from django.db import models
from django.contrib.auth.models import AbstractUser


class Quiz(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=70)
    answer_count = models.IntegerField(default=3)
    answer_given = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question}, ID = {self.id}"


class Answer(models.Model):
    answer = models.CharField(max_length=70)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="f")

    def save(self, *args, **kwargs):
        if self.quiz.answer_count > self.quiz.answer_given:
            self.quiz.answer_given += 1
            self.quiz.save()
            super(Answer, self).save(*args, **kwargs)
        else:
            raise SystemError("answer_count is not equal!!!")
    
    def __str__(self):
        return f"Question = {self.quiz}, Answer = {self.answer}"


class User(AbstractUser):
    age = models.IntegerField(null=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profiles/images/", null=True)
    ex = models.IntegerField(default=0)
    lvl = models.IntegerField(default=1)


class Result(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    solved_questions = models.IntegerField(default=0)
    field_questions = models.IntegerField(default=0)


class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friendship = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendships")
