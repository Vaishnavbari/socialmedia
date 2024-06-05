from django.db import models
from django.contrib.auth.models import AbstractUser


class user_registration(AbstractUser):
    pass


class post(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE )
    title = models.CharField(max_length=100 , blank=True, null=True , default=None)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None ,blank=True, null=True , default=None)
    caption = models.CharField(max_length=1000, blank=True, null=True , default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class like(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    post_id = models.ForeignKey(post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class comment(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    comments = models.CharField( max_length=50,blank=True, null=True , default=None)
    post_id = models.ForeignKey(post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    

    