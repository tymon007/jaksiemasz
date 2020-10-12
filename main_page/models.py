from django.db import models


# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=200, help_text="Type your username here")
    email = models.EmailField(help_text="Type your email here")
    password = models.CharField(max_length=200, help_text="Type your password here")
    salt = models.CharField(max_length=200, help_text="Salt for password", default="")
