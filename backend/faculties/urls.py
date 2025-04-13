from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacultyImportView, GetFacultyView, AddFacultyView, UpdateFacultyView, DeleteFacultyView

urlpatterns = [
    path('import/', FacultyImportView.as_view(), name='faculty-import'),
    path('get-faculty/', GetFacultyView.as_view(), name='get-faculty'),
    path('add-faculty/', AddFacultyView.as_view(), name='add-faculty'),
    path('update-faculty/', UpdateFacultyView.as_view(), name='update-faculty'),
    path('delete-faculty/', DeleteFacultyView.as_view(), name='delete-faculty'),
]
