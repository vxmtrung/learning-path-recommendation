from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GetRuleView, AddRuleView, UpdateRuleView, DeleteRuleView

urlpatterns = [
    path('get-rule/', GetRuleView.as_view(), name='get_rule'),
    path('add-rule/', AddRuleView.as_view(), name='add_rule'),
    path('update-rule/', UpdateRuleView.as_view(), name='update_rule'),
    path('delete-rule/', DeleteRuleView.as_view(), name='delete_rule'),
]
