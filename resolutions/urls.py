from django.urls import path
from . import views

app_name = "resolutions"

urlpatterns = [
    path("select_roles/", views.select_roles, name="select_roles"),
    path("select_causes/", views.select_causes, name="select_causes"),
    path("select_resolutions/", views.select_resolutions, name="select_resolutions"),
    path("personal_list/", views.personal_list, name="personal_list"),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]
