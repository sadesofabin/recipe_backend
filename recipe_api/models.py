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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_recipes')
    title = models.CharField(max_length=255)  # Title of the saved recipe
    ingredients = models.TextField()  # Ingredients for the recipe
    instructions = models.TextField()  # Cooking instructions
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when saved
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when last updated
    deleted_at = models.DateTimeField(null=True, blank=True)  # Timestamp for when the recipe is deleted

    class Meta:
        db_table = 'saved_recipes'  # Optional: Specify the table name if you want to customize it
    
    def __str__(self):
        return f"Saved Recipe: {self.title} by {self.user.username}"