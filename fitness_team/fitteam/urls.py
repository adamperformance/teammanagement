from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name="register"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('basicinfo', views.basicinfo, name='basicinfo'),
    path('profile', views.profile, name="profile"),
    path('before_after', views.before_after, name="before_after"),
    path('upload', views.upload, name="upload"),
    path('bodyweight', views.bodyweight, name="bodyweight"),
    path('nutrition', views.nutrition, name="nutrition"),
    path('chat', views.chat, name="chat"),

    # API
    path('picture', views.picture, name="picture"),
    path('bw_api', views.bw_api, name="bw_api")
]
