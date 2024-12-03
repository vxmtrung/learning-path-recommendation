from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MajorImportView, MajorListView

urlpatterns = [
    path('import/', MajorImportView.as_view(), name='major-import'),
    path('get-majors-by-faculty/', MajorListView.as_view(), name='get-majors-by-faculty'),
]
