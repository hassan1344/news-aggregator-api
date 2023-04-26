from django.urls import path
from aggregator import views

urlpatterns = [
    path('news', views.fetch_news, name='list_articles'),
    path('news/', views.search_news, name='search_articles'),
    path('news/favourite/', views.mark_as_favorite, name='mark_as_favourite')
]