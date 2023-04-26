from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
import json
from aggregator.models import NewsArticle,UserArticle

class NewsApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = 'test'
        self.password = 'test'
        self.article_id = 1
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_general_news_api(self):
        response = self.client.get('/news')
        self.assertEqual(response.status_code, 200)
        news_data = json.loads(response.content)
        self.assertIsInstance(news_data, list)

        for news_item in news_data:
            self.assertIsInstance(news_item['headline'], str) 
            self.assertIsInstance(news_item['link'], str)  
            self.assertIsInstance(news_item['source'], str) 

    def test_news_search_api(self):
        response = self.client.get('/news', {'query': 'bitcoin'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))
        for news in response.json():
            self.assertTrue(isinstance(news, dict))
            self.assertIn('headline', news)
            self.assertIn('link', news)
            self.assertIn('source', news)
    
    def test_mark_article_as_favorite(self):
        news_article = NewsArticle.objects.create(
            headline='Test Headline',
            link='http://test.com',
            source='Test Source',
            query='Test query',
            user=self.user
        )
        UserArticle.objects.create(
            user=self.user,
            query='Test query',
            article= news_article,
            favorite=False
        )
        response = self.client.post('/news/favourite?user={}&id={}'.format('test',1))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['user'], str(self.user))
        self.assertEqual(data['favorite'], True)
        self.assertEqual(data['id'], self.article_id)
        self.assertEqual(data['headline'], 'Test Headline')
        self.assertEqual(data['link'], 'http://test.com')
        self.assertEqual(data['source'], 'Test Source')
    
    def test_mark_article_as_un_favorite(self):
        news_article = NewsArticle.objects.create(
            headline='Test Headline',
            link='http://test.com',
            source='Test Source',
            query='Test query',
            user=self.user
        )
        UserArticle.objects.create(
            user=self.user,
            query='Test query',
            article= news_article,
            favorite=True
        )
        response = self.client.post('/news/favourite?user={}&id={}'.format('test',1))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['user'], str(self.user))
        self.assertEqual(data['favorite'], False)
        self.assertEqual(data['id'], self.article_id)
        self.assertEqual(data['headline'], 'Test Headline')
        self.assertEqual(data['link'], 'http://test.com')
        self.assertEqual(data['source'], 'Test Source')

    def test_get_fav_articles(self):
        news_article = NewsArticle.objects.create(
            headline='Test Headline',
            link='http://test.com',
            source='Test Source',
            query='Test query',
            user=self.user
        )
        UserArticle.objects.create(
            user=self.user,
            query='Test query',
            article= news_article,
            favorite=True
        )

        response = self.client.get('/news/favourite?user={}'.format('test'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(data[0]['id'], self.article_id)
        self.assertEqual(data[0]['headline'], 'Test Headline')
        self.assertEqual(data[0]['link'], 'http://test.com')
        self.assertEqual(data[0]['source'], 'Test Source')