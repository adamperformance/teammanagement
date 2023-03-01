from django.contrib import admin

from .models import User, BasicInfo, ProgressPics

# Register your models here.

admin.site.register(User)
admin.site.register(BasicInfo)
admin.site.register(ProgressPics)