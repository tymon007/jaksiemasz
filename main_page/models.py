from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=200, help_text="Type your username here")
    email = models.EmailField(help_text="Type your email here")
    password = models.CharField(max_length=200, help_text="Type your password here")
    salt = models.CharField(max_length=200, help_text="Salt for password", default="")

    def __str__(self):
        return '%s' % self.username


class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(help_text="It is text describing user's problem here")
    well_being = models.IntegerField(help_text="It is numeric representation of well-being")
    food = models.IntegerField(help_text="It is numeric representation of food")
    date = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now, help_text="This is date when"
                                                                                                    "post was added")
    icon = models.CharField(max_length=200, help_text="This is name of icon file")
