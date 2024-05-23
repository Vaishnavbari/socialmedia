from django.db import models
from django.contrib.auth.models import AbstractUser


class user_registration(AbstractUser):
    pass


class post(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    caption = models.CharField(max_length=1000)

class like(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    post_id = models.ForeignKey(post, on_delete=models.CASCADE)


class comment(models.Model):
    user = models.ForeignKey(user_registration, on_delete=models.CASCADE)
    comments = models.CharField( max_length=50)
    post_id = models.ForeignKey(post, on_delete=models.CASCADE)

    

    