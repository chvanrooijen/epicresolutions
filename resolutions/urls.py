from django.urls import path
from . import views

app_name = 'resolutions'

urlpatterns = [
    path('select_role/', views.select_role, name='select_role'),
    path('select_cause/', views.select_cause, name='select_cause'),
    path('select_resolutions/', views.select_resolutions, name='select_resolutions'),
    path('personal_list/', views.personal_list, name='personal_list'),
]