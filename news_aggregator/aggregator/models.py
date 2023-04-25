from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    source = models.CharField(max_length=50)

class UserFavorite(models.Model):
    user = models.CharField(max_length=50)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)