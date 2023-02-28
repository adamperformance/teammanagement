from django.contrib import admin

from .models import User, BasicInfo

# Register your models here.

admin.site.register(User)
admin.site.register(BasicInfo)