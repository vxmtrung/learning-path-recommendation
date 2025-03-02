from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GetStudentNeedView, CreateStudentNeedView

urlpatterns = [
    path('get-student-need/', GetStudentNeedView.as_view(), name='get-student-need'),
    path('create-student-need/', CreateStudentNeedView.as_view(), name='create-student-need')
]
