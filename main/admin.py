from django.contrib import admin
from django.contrib.auth.models import Group, User
from main.models import Profile, Products, Post, Image

# Unregister Group
# admin.site.unregister(Group)
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Products)
