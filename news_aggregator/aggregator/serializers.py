from rest_framework import serializers
from aggregator.models import NewsArticle,UserArticle

class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewsArticle
        fields=['headline','link','source','user']

class UserArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserArticle
        fields=['user','article','favorite','query']