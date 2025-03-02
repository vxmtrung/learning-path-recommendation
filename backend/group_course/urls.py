from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupCourseImportView, GroupCourseGetView

urlpatterns = [
    path('import/', GroupCourseImportView.as_view(), name='group-course-import'),
    path('get-group-course/', GroupCourseGetView.as_view(), name='group-course-get'),
]
