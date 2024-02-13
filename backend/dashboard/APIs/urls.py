from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadFunction, name='upload'),
    # Add more URL patterns as needed
]