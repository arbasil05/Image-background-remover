# urls.py
from django.contrib import admin
from django.urls import path
from background_remover import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('action', views.action),
    path('download', views.download_image, name='download_image'),  # Updated the name here
]
