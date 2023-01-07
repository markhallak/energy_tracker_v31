from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length = 100)
    code = models.CharField(max_length = 3)

class User(AbstractUser):
    username = None
    name = models.CharField(max_length = 100)
    #last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 254, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    #profile_image = models.FilePathField(path="/assets/img/profile",null = True, default = None)
    def __str__(self):
        return self.email

