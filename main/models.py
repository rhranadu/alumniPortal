from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from ckeditor.fields import RichTextField
from datetime import datetime
# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user/avatar', default="..\static\assets\img\profile\default-profile-photo.jpg")
    bio = models.TextField(max_length= 500, blank = True, default="")
    career_position = models.CharField(max_length=50, null=True, blank= True, default="Student")
    state = models.CharField(max_length=20, blank= True, null=True)
    country = models.CharField(max_length=20, blank= True, null=True)
    linkedin_url = models.CharField(max_length=255, blank= True, null=True)
    instagram_url = models.CharField(max_length=255, blank= True, null=True)
    twitter_url = models.CharField(max_length=255, blank= True, null=True)
    last_updated = models.DateTimeField(User, auto_now=True)
    def __str__(self):
        return self.user.email

def create_profile(sender,instance, created, **kwargs):
    if created:
        user_profile = Profile(user= instance)
        user_profile.save()
post_save.connect(create_profile, sender= User)    

class Image(models.Model):
    caption = models.CharField(max_length=20)
    photo   = models.ImageField(upload_to='user/images')
    def __str__(self):
        return (f'{self.caption}', f'{self.photo}')
# Posts
class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.DO_NOTHING)
    body = RichTextField(blank=True, null=True)
    synopsis = models.CharField(max_length=100, default="Place holder")
    created_at = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return (f"{self.user}"
                f"({self.created_at})"
                f"{self.synopsis}")
# Feedbacks
class Feedback(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    comment= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="feedbacks", on_delete=models.DO_NOTHING)
# Products 
class Products(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100) 
    product_category = models.CharField(max_length=100, default="") 
    product_subcategory = models.CharField(max_length=50, default="") 
    product_price = models.IntegerField()
    product_desc = models.CharField(max_length=300)
    product_image = models.ImageField(upload_to='shop/images', default="")
    

