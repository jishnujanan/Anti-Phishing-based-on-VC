from django.contrib import admin

from website import models

admin.site.register(models.User)
admin.site.register(models.Captcha)
