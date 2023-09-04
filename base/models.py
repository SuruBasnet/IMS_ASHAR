from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserInfo(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    username = models.CharField(unique=True,max_length=200)