from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username