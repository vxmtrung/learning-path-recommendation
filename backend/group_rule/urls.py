from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GetRuleByGroupCourseView, AddNewRuleToGroupCourseView, UpdateRuleToGroupCourseView, DeleteRuleToGroupCourseView
urlpatterns = [
    path('get-rule-by-group-course/', GetRuleByGroupCourseView.as_view(), name='get_rule_by_group_course'),
    path('add-new-rule-to-group-course/', AddNewRuleToGroupCourseView.as_view(), name='add_new_rule_to_group_course'),
    path('update-rule-to-group-course/', UpdateRuleToGroupCourseView.as_view(), name='update_rule_to_group_course'),
    path('delete-rule-to-group-course/', DeleteRuleToGroupCourseView.as_view(), name='delete_rule_to_group_course')
]
