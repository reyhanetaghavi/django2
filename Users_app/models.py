from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=30)
    family_name = models.CharField(max_length=30)

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = ['name', 'family_name'] 

    def __str__(self):
        return self.phone_number


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    family_name = models.CharField(max_length=30)
    GENDER = [
        ('خانم','خانم'), ('آقا','آقا')
    ]
    gender = models.CharField(choices=GENDER,max_length=4,default='آقا')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user.name = self.name
        self.user.family_name = self.family_name

    def __str__(self):
        return f"{self.user.phone_number}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()



