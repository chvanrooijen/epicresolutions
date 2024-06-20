from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
        path('news/', views.news, name='news'),
        path('search/', views.search, name='search'),
        path('news/<int:article_id>/', views.news_article, name='news_article'),
]