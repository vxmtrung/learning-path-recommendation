from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupCourseImportView, GroupCourseGetView, AddGroupCourseView, DeleteGroupCourseView, UpdateGroupCourseView

urlpatterns = [
    path('import/', GroupCourseImportView.as_view(), name='group-course-import'),
    path('get-group-course/', GroupCourseGetView.as_view(), name='group-course-get'),
    path('add-group-course/', AddGroupCourseView.as_view(), name='group-course-add'),
    path('update-group-course/', UpdateGroupCourseView.as_view(), name='group-course-update'),
    path('delete-group-course/', DeleteGroupCourseView.as_view(), name='group-course-delete'),
]
