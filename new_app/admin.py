from django.contrib import admin

from new_app import models

# Register your models here.

admin.site.register(models.Login)

admin.site.register(models.reader)

admin.site.register(models.author)

admin.site.register(models.book)

admin.site.register(models.Borrow)

admin.site.register(models.Review)
