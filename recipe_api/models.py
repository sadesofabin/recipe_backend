from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')  
    email = models.EmailField(unique=True)  
    firstname = models.CharField(max_length=100, blank=True, null=True)  
    lastname = models.CharField(max_length=100, blank=True, null=True)   
    phonenumber = models.CharField(max_length=15, unique=True, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.user.username  


class RecipeApiUserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to auth_user
    additional_info = models.TextField()  # Example field
