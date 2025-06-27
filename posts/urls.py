from django.urls import path
from . import views
from .views import PostListView, PostDetailView

app_name = "posts"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("category/<int:pk>/", views.category_filter_pk, name="category_filter_pk"),
    path("category/<slug:slug>/", views.category_filter, name="category_filter"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
]