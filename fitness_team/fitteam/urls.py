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

    # API
    path('picture', views.picture, name="picture")
]
