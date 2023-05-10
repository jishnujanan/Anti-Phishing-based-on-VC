from django.db import models

class User(models.Model):
    fullname = models.CharField(max_length=30,default="fullname of the user")
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username