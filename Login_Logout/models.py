from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomManager
from django.utils.translation import gettext_lazy as _

from django.urls import reverse

 
class User(AbstractUser): 
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length= 200)
    is_author = models.BooleanField(default=False)  
    objects = CustomManager()
  
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
    

    def __str__(self):
        return self.email
 
  
    
    
    