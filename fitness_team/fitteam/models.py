from django.db import models
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    pass

class BasicInfo(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
        )

    user = models.OneToOneField(User, primary_key=True, blank=True, related_name="basic", on_delete=models.CASCADE)
    sex = models.CharField(max_length=64, choices=SEX)
    date_of_birth = models.DateField()
    height = models.PositiveIntegerField()
    profile_pic = models.ImageField(default="profile.jpg")

    def age(self):
        today = timezone.now().date()
        birth = self.date_of_birth
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age

