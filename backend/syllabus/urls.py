from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SyllabusImportView, SyllabusListView

urlpatterns = [
    path('import/', SyllabusImportView.as_view(), name='syllabus-import'),
    path('get-syllabus-by-course/', SyllabusListView.as_view(), name='get-syllabus'),
]
