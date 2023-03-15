
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('profile/',views.profile,name="profile"),
    #path('login/',auth_views.LoginView.as_view(template_name="users/login.html"),name="login"),
    #path('logout/',auth_views.LogoutView.as_view(template_name="users/logout.html"),name="logout"),
]










