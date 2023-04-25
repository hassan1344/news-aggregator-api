from django.db import models

class NewsArticle(models.Model):
    class Meta:
        db_table="news_article"

    headline = models.CharField(max_length=200)
    url = models.URLField()
    source = models.CharField(max_length=50)

class UserFavorite(models.Model):
    class Meta:
        db_table="user_favorites"
        
    user = models.CharField(max_length=50)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)