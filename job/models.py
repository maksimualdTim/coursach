from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    minBounty = models.IntegerField(blank=True)
    maxBounty = models.IntegerField(blank=True)
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Category(models.Model):
    title = models.CharField(max_length=250)


class Profile(models.Model):
    EMPLOYER = 'e'
    CANDIDATE = 'c'

    USER_TYPES = (EMPLOYER, CANDIDATE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=USER_TYPES)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
