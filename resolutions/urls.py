from django.urls import path
from . import views

app_name = "resolutions"

urlpatterns = [
    # New workflow
    path("", views.introduction, name="introduction"),
    path("consumer-resolutions/", views.select_consumer_resolutions, name="select_consumer_resolutions"),
    path("roles/", views.select_other_roles, name="select_other_roles"),
    path("applicable-resolutions/", views.further_personalise_list, name="further_personalise_list"),
    path("personal-list/", views.personal_list_new, name="personal_list_new"),
    path("generate-pdf/", views.generate_pdf, name="generate_pdf"),
]
