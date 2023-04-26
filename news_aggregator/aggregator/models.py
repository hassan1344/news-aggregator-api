from django.db import models

class NewsArticle(models.Model):
    class Meta:
        db_table="news_article"

    query = models.CharField(max_length=50, default='')
    headline = models.CharField(max_length=200)
    link = models.URLField()
    source = models.CharField(max_length=50)
    user = models.CharField(max_length=50,default='')

class UserArticle(models.Model):
    class Meta:
        db_table="user_articles"
        
    user = models.CharField(max_length=50)
    query= models.CharField(max_length=50, default='')
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)