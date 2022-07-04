from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    minBounty = models.IntegerField(blank=True, null=True)
    maxBounty = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.CASCADE)


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)

