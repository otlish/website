from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
#from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    objects = UserManager()
    username=models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    #phone_number=PhoneNumberField(blank=True,null=True,unique=True)

