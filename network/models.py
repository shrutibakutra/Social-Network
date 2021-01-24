from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Post(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User,blank=True,related_name="likedBy")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    like  = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="liked_by")
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    postBy = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posted_by")


class Follow(models.Model):
    follow  = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
