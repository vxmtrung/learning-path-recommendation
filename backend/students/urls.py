from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentImportView, StudentListView, AddStudentView, UpdateStudentView, DeleteStudentView

urlpatterns = [
    path('import/', StudentImportView.as_view(), name='student-import'),
    path('get-student-info/', StudentListView.as_view(), name='student-info'),
    path('add-student/', AddStudentView.as_view(), name='add-student'),
    path('update-student/', UpdateStudentView.as_view(), name='update-student'),
    path('delete-student/', DeleteStudentView.as_view(), name='delete-student')
]
