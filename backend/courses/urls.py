from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseImportView, AddCourseView, GetCourseView, UpdateCourseView, DeleteCourseView, GetCoureByGroupCourseView, AddCourseToGroupCourseView, RemoveCourseFromGroupCourseView
urlpatterns = [
    path('import/', CourseImportView.as_view(), name='course-import'),
    path('add-course/', AddCourseView.as_view(), name='course-add'),
    path('get-course/', GetCourseView.as_view(), name='course-get'),
    path('update-course/', UpdateCourseView.as_view(), name='course-update'),
    path('delete-course/', DeleteCourseView.as_view(), name='course-delete'),
    path('get-course-by-group-course/', GetCoureByGroupCourseView.as_view(), name='course-get-by-group-course'),
    path('add-course-to-group-course/', AddCourseToGroupCourseView.as_view(), name='course-add-to-group-course'),
    path('remove-course-from-group-course/', RemoveCourseFromGroupCourseView.as_view(), name='course-remove-from-group-course')
]
