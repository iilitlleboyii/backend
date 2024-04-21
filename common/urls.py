from django.urls import path
from common.views import UploadFile, DownloadFile

urlpatterns = [
    path('upload/', UploadFile.as_view(), name='file'),
    path('download/', DownloadFile.as_view(), name='file'),
]
