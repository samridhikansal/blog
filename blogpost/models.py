from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class PostCategory(models.Model):
    category = models.CharField(max_length=50 ,default = "General" )

    def __str__(self):
        return self.category

class Post(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(max_length=500)
    image = models.ImageField(upload_to= "image/", blank=True , default= "cow.jpg")
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, null=True, blank= True)
   

    def __str__(self):
        return self.name
    

class Comments(models.Model):
    comment = models.TextField(max_length=100)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, blank=True, null=True)

