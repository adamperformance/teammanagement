from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import User, BasicInfo, ProgressPics

import datetime

# Create your views here.


# @allowed_users(allowed_roles=['ROLENAME']) <-- this can be used to separate the superuser and the user
# ROLENAME eg 'customer'
# @login_required(login_url='login')

def index(request):
    
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "fitteam/index.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def basicinfo(request):

    if request.method == "POST":
        user = User.objects.get(username=request.user)
        user.last_name = request.POST["last_name"]
        user.first_name = request.POST["first_name"]
        user.save()

        height = request.POST["height"]
        sex = request.POST["sex"]
        date_of_birth = request.POST["date_of_birth"]
        profile_pic = request.FILES["profile_pic"]

        try:
            basic = BasicInfo.objects.get(pk=user.id)
            basic.sex = sex
            basic.height = height
            basic.date_of_birth = date_of_birth
            basic.profile_pic = profile_pic
            basic.save()
        except ObjectDoesNotExist:
            basic = BasicInfo(user=user, sex=sex, height=height, date_of_birth=date_of_birth, profile_pic=profile_pic)
            basic.save()

        return render(request, 'fitteam/test.html', {
            "user": user,
            "other": basic
        })
    else:
        return render(request, 'fitteam/basicinfo.html')


def profile(request):
    return render(request, "fitteam/profile_page.html")

def before_after(request):

    return render(request, "fitteam/before_after.html")

def upload(request):

    if request.method == 'POST':
        progress_pic = ProgressPics()
        progress_pic.user = request.user
        if request.POST["date"] != "":
            progress_pic.date = request.POST["date"]
        else:
            progress_pic.date = datetime.datetime.now()
        progress_pic.progress_pic = request.FILES["progress_pic"]
        progress_pic.save()
        return HttpResponseRedirect(reverse('before_after'))
    else:
        return render(request, 'fitteam/upload.html', {
        })

def login_view(request):

    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "fitteam/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "fitteam/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def register(request):
        
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]

    # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "fitteam/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "fitteam/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    return render(request, "fitteam/register.html", {
        "message": ""
    })