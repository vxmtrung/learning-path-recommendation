"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
  openapi.Info(
    title="Learning Path Recommendation APIs",
    default_version="v1",
    description="API Docs For Learning Path Recommendation System",
  ),
  public=True,
  permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('faculties/', include('faculties.urls')),
    path('majors/', include('majors.urls')),
    path('courses/', include('courses.urls')),
    path('students/', include('students.urls')),
    path('learnlogs/', include('learnlog.urls')),
    path('recommend/', include('recommend.urls')),
    path('predict/', include('predict.urls')),
    path('recommendlogs/', include('recommendlogs.urls')),
    path('group-course/', include('group_course.urls')),
    path('learning-outcomes/', include('learning_outcomes.urls')),
    path('student-needs/', include('student_needs.urls')),
    path('scheduled-tasks/', include('scheduler.urls')),
    path('evaluations/', include('evaluations.urls')),
    path('semesters/', include('semesters.urls')),
    path('rules/', include('rules.urls')),
    path('group-rules/', include('group_rule.urls')),
]
