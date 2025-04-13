from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MajorImportView, MajorListView, GetMajorView, AddMajorView, UpdateMajorView, DeleteMajorView

urlpatterns = [
    path('import/', MajorImportView.as_view(), name='major-import'),
    path('get-majors-by-faculty/', MajorListView.as_view(), name='get-majors-by-faculty'),
    path('get-major/', GetMajorView.as_view(), name='get-major'),
    path('add-major/', AddMajorView.as_view(), name='add-major'),
    path('update-major/', UpdateMajorView.as_view(), name='update-major'),
    path('delete-major/', DeleteMajorView.as_view(), name='delete-major')
]
