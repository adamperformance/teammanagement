from django.db import models
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.username})"
    

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
    
    def __str__(self):
        return f"{self.user.username} basic"

class BodyComposition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    bodyweight = models.FloatField()
    bodyfat = models.FloatField(default=0)

    @property
    def fm(self):
        if self.bodyfat == 0:
            return "Adj meg testzsír százalékt a számításhoz!"
        elif self.bodyfat != 0:
            return "{:.2f}".format(self.bodyweight * self.bodyfat/100)
        
    @property
    def ffm(self):
        if self.bodyfat == 0 and self.waist != 0:
            return "Adj meg testzsír százalékt a számításhoz!"
        elif self.bodyfat != 0:
            return "{:.2f}".format(self.bodyweight - self.bodyweight * self.bodyfat/100)


class ProgressPics(models.Model):
    DIR = (
    ('Front', 'Front'),
    ('Side', 'Side'),
    ('Back','Back')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    progress_pic = models.ImageField(upload_to="progress_pics")
    pic_direction = models.CharField(null=True, max_length=64, choices=DIR)

    def __str__(self):
        return f"{self.user.username} {self.date} {self.pic_direction}"