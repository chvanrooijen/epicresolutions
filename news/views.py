from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
# from django.http import Http404
from .models import NewsArticle

# Create your views here.
def news(request):
    news_articles = NewsArticle.objects.order_by('-pub_date')
    paginator = Paginator(news_articles, 5) # Show 5 articles per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news.html', {'page_obj': page_obj})

def news_article(request, article_id):
    article = get_object_or_404(NewsArticle, pk=article_id)
    return render(request, 'news/news_article.html', {'article': article})

def search(request):
    query = request.GET.get('q')
    articles_list = NewsArticle.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator = Paginator(articles_list, 10)  # Show 10 articles per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/search.html', {'page_obj': page_obj, 'query': query})

