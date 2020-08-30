from django.db import models

# Create your models here.

class Person(models.Model):

    MAN = 0
    WOMAN = 1

    HOKKAIDO = 0
    TOHOKU = 5
    TOKYO = 10
    CHIBA = 11
    KANAGAWA = 12
    SAITAMA = 13
    TOCHIGI = 14
    IBARAGI = 15
    CHUBU = 20
    KANSAI = 25
    CHUGOKU = 30
    SHIKOKU = 35
    KYUSHU = 40
    OKINAWA = 45

    # 名前
    name = models.CharField(max_length=128)

class User(models.Model):
    primkey=models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    logindate=models.DateTimeField(auto_now=True)


class Diaries(models.Model):
    primkey=models.IntegerField(primary_key=False)
    article = models.CharField(max_length=1000)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

class UserFriends(models.Model):
    userid=models.IntegerField(primary_key=False)
    friendid=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

