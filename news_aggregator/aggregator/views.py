import requests
from rest_framework.response import Response
from rest_framework import status
from news_aggregator.settings import REDDIT_API_URL,NEWS_API_URL,NEWS_API_SECRET
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def fetch_news(request):

    try:
        reddit_api_response= requests.get('{}?q="Pakistan"&sort=top&limit=10'.format(REDDIT_API_URL))
        news_api_response= requests.get(
                                '{}?q="Pakistan"&pageSize=10'.format(NEWS_API_URL),
                                headers= {'Authorization': 'Bearer {}'.format(NEWS_API_SECRET)}
                                )
        
        if reddit_api_response.status_code == 200 and news_api_response.status_code == 200:
            reddit_api_data = reddit_api_response.json()
            news_api_data = news_api_response.json()
            reddit_api_res = [{'headline': post["data"]["title"], 'link': post["data"]["url_overridden_by_dest"], 'source': "reddit"} for post in reddit_api_data["data"]["children"]]
            news_api_res = [{'headline': article["title"], 'link': article["url"], 'source': "newsapi"} for article in news_api_data["articles"]]
            return Response((news_api_res + reddit_api_res), status=status.HTTP_200_OK)
        
        elif reddit_api_response.status_code == 200:
            reddit_api_data = reddit_api_response.json()
            reddit_api_res = [{'headline': post["data"]["title"], 'link': post["data"]["url_overridden_by_dest"], 'source': "reddit"} for post in reddit_api_data["data"]["children"]]
            return Response(reddit_api_res, status=status.HTTP_200_OK)
        
        elif news_api_response.status_code == 200:
            news_api_data = news_api_response.json()
            news_api_res = [{'headline': article["title"], 'link': article["url"], 'source': "newsapi"} for article in news_api_data["articles"]]
            return Response(news_api_res, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Unable to retrieve news from any source.'}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception:
        return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)