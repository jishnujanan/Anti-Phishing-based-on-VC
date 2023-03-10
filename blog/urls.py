from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users import views as users_views

urlpatterns = [
    path('',views.home,name="blog-home"),
    path('register/',users_views.register,name="register"),
    path('profile/',users_views.profile,name="profile"),
    path('login/',auth_views.LoginView.as_view(template_name="users/login.html"),name="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name="users/logout.html"),name="logout"),
    path('about/',views.about,name="blog-about"),
]
