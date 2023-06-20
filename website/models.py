from django.db import models

class User(models.Model):
    fullname = models.CharField(max_length=30,default="fullname of the user")
    username = models.CharField(max_length=50,unique=True,primary_key=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username

class Captcha(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,default="")
    captcha_1=models.CharField(max_length=50)
    captcha_2=models.CharField(max_length=50)
    captcha_3=models.CharField(max_length=50)
    captcha_4=models.CharField(max_length=50)
    captcha_5=models.CharField(max_length=50)
    captcha_6=models.CharField(max_length=50)
    captcha_7=models.CharField(max_length=50)
    captcha_8=models.CharField(max_length=50)

    