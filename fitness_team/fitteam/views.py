from django.shortcuts import render
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
import json

from .models import User, BasicInfo, ProgressPics, BodyComposition

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

    user = User.objects.get(username=request.user.username)
    pics = user.progresspics_set.all()

    dates = []

    for pic in pics:
        x = pic.date
        date = x.strftime('%b. %-d, %Y')
        if date not in dates:
            dates.append(date)

    return render(request, "fitteam/before_after.html", {
        "dates":dates
    })


def bodyweight(request):

    user = request.user.username
    user = User.objects.get(username=user)

    try:
        bw_data = user.bodycomposition_set.all().order_by('-date')
        bw_reverse = user.bodycomposition_set.all().order_by('date')
    except ObjectDoesNotExist:
        bw_data = ""

    number = []
    for i in range(len(bw_data)):
        number.append(i)
        i += 1

    x = 1
    wght = 0
    dates = []
    measures = []

    # if you have multiple input for 1 day, this will average it out
    for i in range(len(bw_reverse)):
        tmp = bw_reverse[i]
        if i < (len(bw_reverse)-1) and tmp.date == bw_reverse[i+1].date:
            x = x + 1
            wght = wght + tmp.bodyweight
        else:
            wght = wght + tmp.bodyweight
            a = wght / x
            measures.append(a)
            dates.append(tmp.date)
            wght = 0
            x = 1
        i += 1

    if request.method == "POST":
        if "add" in request.POST:
            bodyweight = request.POST["bodyweight"]
            date = request.POST["date"]
            bodyfat = request.POST["bodyfat"]
            if bodyfat == "":
                bodyfat = 0
            if date == "":
                date = timezone.now().date()
            bw = BodyComposition(user=user, date=date, bodyweight=bodyweight, bodyfat=bodyfat)
            bw.save()
            return HttpResponseRedirect('bodyweight', {
                "weights": bw_data,
                "numbers":number,
                "dates": dates,
                "measures":measures
            })
        else:
            # delete functionality does not work due to a change in the date (from Charfield to DateField)
            for date in dates:
                for measure in measures:
                    measure = float(measure)
                    if f"delete{date}{measure}" in request.POST:
                        to_delete = BodyComposition.objects.filter(user=user, date=date, bodyweight=measure)
                        to_delete.delete()

            return HttpResponseRedirect('bodyweight', {
                "weights": bw_data,
                "numbers":number,
                "dates": dates,
                "measures":measures
            })
    else:
        return render(request, 'fitteam/bodyweight.html', {
            "weights": bw_data,
            "dates": dates,
            "measures":measures
        })

def upload(request):

    # additional functionality needed - check if there is already and input for the given day
    # if there is, overwrite that - 1 triplet of pictures / day!

    if request.method == 'POST':
        progress_pic = ProgressPics()
        progress_pic.user = request.user
        if request.POST["date"] != "":
            progress_pic.date = request.POST["date"]
        else:
            progress_pic.date = datetime.datetime.now()
        progress_pic.pic_direction = request.POST["direction"]
        progress_pic.progress_pic = request.FILES["progress_pic"]
        progress_pic.save()
        return HttpResponseRedirect(reverse('before_after'))
    else:
        return render(request, 'fitteam/upload.html', {
        })


def bw_api(request):
    user = request.user
    bws = BodyComposition.objects.filter(user=user).order_by('date')

    bodyweights = []

    for bw in bws:        
        # format date properly and create a list of the disctinct dates 
        y = bw.date
        date = y.strftime('%b. %-d, %Y')

        x = {}
        x["date"] = date
        x["bodyweight"] = bw.bodyweight
        x["bodyfat"] = bw.bodyfat

        bodyweights.append(x)
 
    
    # return render(request, "fitteam/tits.html", {
    #     "pic":bws,
    #     "dates":list_of_dates,
    #     "luck":list_of
    # })

    return JsonResponse(bodyweights, safe=False)

def picture(request):
    user = request.user
    pics = ProgressPics.objects.filter(user=user).order_by('date')

    list_of_dates = []
    pictures = {}

    list_of = []
    x = {"front":"","side":"","back":""}

    for pic in pics:

        # create dictionary of pic triplets {'front':url1,'side':url2,'back':url3}
        if pic.pic_direction == "Front":
            x["front"] = pic.progress_pic.url
        elif pic.pic_direction == "Side":
            x["side"] = pic.progress_pic.url
        elif pic.pic_direction == "Back":
            x["back"] = pic.progress_pic.url

        if x["front"] != "" and x["side"] != "" and x["back"] != "":
            list_of.append(x)
            x = {"front":"","side":"","back":""}
        
        # format date properly and create a list of the disctinct dates
        y = pic.date
        date = y.strftime('%b. %-d, %Y')

        if date not in list_of_dates:  
            list_of_dates.append(date)
    
    # create a dictionary where the keys are the dates and the values are the picture triplets
    for i in range(len(list_of_dates)):
        pictures[list_of_dates[i]]=list_of[i]
    
    # return render(request, "fitteam/tits.html", {
    #     "pic":list_of_dates,
    #     "dates":list_of,
    #     "luck":pictures
    # })

    return JsonResponse(pictures)


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