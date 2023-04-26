from django.urls import path
from aggregator import views

urlpatterns = [
    path('news', views.fetch_news, name='list_articles'),
    path('news/favourite', views.process_favorite_news, name='process_favorite_articles'),
]