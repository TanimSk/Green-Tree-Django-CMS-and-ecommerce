from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

class Post(models.Model):
    user = models.IntegerField(null=False, default=0)
    category = models.CharField(max_length=20, default='Not given')
    title = models.CharField(max_length=250, default='Not given')
    img = models.ImageField(upload_to = "images/", null=True, default=None)
    description = models.TextField(default='Not given')
    vacancy = models.IntegerField(default=1)

class OrderList(models.Model):
    user = models.IntegerField(null=False, default=0)
    product_id = models.IntegerField(null=False, default=0)

class PlacedOrder(models.Model):
    name = models.CharField(max_length=20, default='Not given')
    address = models.CharField(max_length=100, default='Not given')
    phone_no = models.CharField(max_length=20, default='Not given')
    products = models.CharField(max_length=200, default='0')

class Comment(models.Model):
    post_id = models.IntegerField(null=False, default=0)
    name = models.CharField(max_length=100, default='User')
    comment = models.TextField(default='No Comment')

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()