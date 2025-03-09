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
from django.urls import path, include

urlpatterns = [
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
    path('evaluations/', include('evaluations.urls'))
]
