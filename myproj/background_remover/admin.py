from django.contrib import admin
from .models import UploadedImage,UploadedImageAdmin

admin.site.register(UploadedImage,UploadedImageAdmin)


