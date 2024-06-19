from django.urls import path
from . import views

urlpatterns = [
    path('select_role/', views.select_role, name='select_role'),
    path('select_cause/', views.select_cause, name='select_cause'),
    path('generate_resolutions/', views.generate_resolutions, name='generate_resolutions'),
]