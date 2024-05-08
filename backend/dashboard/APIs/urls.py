from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadFunction, name='upload'),
    path('summary/', views.Summary,name='summary'),
    path('table_summary/', views.Table_Summary, name='table_summary'),
    path('download_data/',views.DownloadData,name='download_data')


    # Add more URL patterns as needed
]