from django.urls import path
from . import views
from .views import PostListView, PostDetailView

app_name = "posts"

urlpatterns = [
    path("post_detail/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post_list", PostListView.as_view(), name="post_list"),
    path("category_filter/<int:pk>/", views.category_filter, name="category_filter"),
]