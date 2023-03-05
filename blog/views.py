from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Post

def home(request):
    data={
        'posts':Post.objects.all(),
        'title':"Blog Title",
        'user':User
    }
    return render(request=request,template_name='blog/home.html',context=data,)

def about(request):
    return render(request=request,template_name='blog/about.html',context={'title':"Blog About"})

def signup(request):
    return render(request=request,template_name='blog/signup.html')