from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.
class About(models.Model):
    name=models.CharField(max_length=50)
    owner= models.CharField(max_length=70)
    company_intro= models.TextField(max_length=2000)
    image = models.ImageField(upload_to="image/", blank=True, null=True, default="cow.jpg")
    def __str__(self):
        return self.name
    
class Author(models.Model):
    image = models.ImageField(upload_to="image/", blank=True, null=True, default="cow.jpg")
    intro = models.TextField(max_length=500, default=" ", null=True, blank="True")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_posts = models.IntegerField(default=0, null=True)
    total_followers= models.IntegerField(default=0 ,null=0, blank=True)
    total_follows= models.IntegerField(default=0, null=0, blank=True)
    category=models.CharField(max_length=20, default="reader")

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    author = models.ForeignKey(User, models.CASCADE)
    follower = models.CharField(max_length=50)
    status= models.BooleanField(default=False)
    
    def __str__(self):
        return self.follower

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
    time = models.DateField(default=datetime.now(), null=True, blank=True)
    total_likes = models.IntegerField(default=0, null=True, blank=True)
    total_dislikes = models.IntegerField(default=0, null=True, blank = True)
    def __str__(self):
        return self.name
    
class Post_like_dislike(models.Model):
    like = models.BooleanField(default=False)
    dislike= models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=50, null=True, default= "Guest")


    

class Comments(models.Model):
    comment = models.TextField(max_length=100)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.comment


class Comments_reply(models.Model):
    reply = models.CharField(max_length = 100)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE )
    author = models.CharField(max_length=50, blank=True, default="Guest", null=True)

    def __str__(self):
        return self.reply



