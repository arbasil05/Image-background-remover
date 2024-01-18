from django.db import models
from django.contrib import admin
from datetime import datetime

current_date = datetime.now()

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    upload_date = models.DateTimeField()

    def save(self,*args,**kwargs):
        self.upload_date = datetime.now()
        super().save(*args,**kwargs)

class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('image','upload_date')

    def __str__(self):
        return f'Image uploaded on {self.upload_date}'
