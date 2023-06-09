import requests
from rest_framework.response import Response
from rest_framework import status
from news_aggregator.settings import REDDIT_API_URL,NEWS_API_URL,NEWS_API_SECRET
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from aggregator.models import NewsArticle,UserArticle
from aggregator.serializers import NewsArticleSerializer,UserArticleSerializer
from datetime import datetime, timedelta
import pytz

#--------------Getting data from reddit API------------------------------------
def get_reddit_api_data(query=None):

    if query == None:

        reddit_api_response= requests.get(
                                '{}?q="Pakistan"&sort=top&limit=10'.format(REDDIT_API_URL),
                                headers={'user-agent': 'your bot 0.1'}
                                )
    else:
        reddit_api_response= requests.get(
                                        '{}?q="{}"&sort=top&limit=10'.format(REDDIT_API_URL,query),
                                        headers={'user-agent': 'your bot 0.1'}
                                        )
    return reddit_api_response
#---------------------------------------------------------------------------------

#-------------Getting data from News API------------------------------------------
def get_news_api_data(query=None):
    if query == None:
        news_api_response= requests.get(
                                '{}?q="Pakistan"&pageSize=10'.format(NEWS_API_URL),
                                headers= {'Authorization': 'Bearer {}'.format(NEWS_API_SECRET)}
                                )
    else:
        news_api_response= requests.get(
                                        '{}?q="{}"&pageSize=10'.format(NEWS_API_URL,query),
                                        headers= {'Authorization': 'Bearer {}'.format(NEWS_API_SECRET)}
                                        )
    return news_api_response
#------------------------------------------------------------------------------------

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def fetch_news(request):
#----------------------Search News (/news?query=)----------------------------------------------------------------------------------------------------------------
    if request.GET:
        try:
            if 'query' not in request.GET:
                return Response({'error' : 'Invalid request parameter'}, status=status.HTTP_400_BAD_REQUEST)
            
            query = request.GET.get('query')
            expiry_time = datetime.now() - timedelta(minutes=60)  # expiry time has been set to 24 hours
            expiry_time = pytz.timezone('UTC').localize(expiry_time)

            reddit_api_response= get_reddit_api_data(query)
            news_api_response= get_news_api_data(query)

            news = UserArticle.objects.filter(user=str(request.user), query=query).first()
    
            if news is not None:
                if news.created_at < expiry_time:
                    print('expired')
                    expired_news = UserArticleSerializer(UserArticle.objects.filter(user=str(request.user),query=query),many=True)

                    if reddit_api_response.status_code == 200 and news_api_response.status_code == 200:
                        reddit_api_data = reddit_api_response.json()
                        news_api_data = news_api_response.json()
                        reddit_api_res = [{'headline': post["data"]["title"], 'link': post["data"]["url"], 'source': "reddit"} for post in reddit_api_data["data"]["children"]]
                        news_api_res = [{'headline': article["title"], 'link': article["url"], 'source': "newsapi"} for article in news_api_data["articles"]]
                        combined_news = news_api_res + reddit_api_res
                        
                        for index,item in enumerate(combined_news):
                            news_article = NewsArticle.objects.filter(query = query, id=expired_news.data[index]["article"]).update(headline = item["headline"], link= item["link"], source= item["source"])
                            UserArticle.objects.filter(article_id=expired_news.data[index]["article"]).update(created_at=datetime.now(pytz.timezone('UTC')))
                        return Response(combined_news, status=status.HTTP_200_OK)
                    
                    elif reddit_api_response.status_code == 200:
                        reddit_api_data = reddit_api_response.json()
                        reddit_api_res = [{'headline': post["data"]["title"], 'link': post["data"]["url"], 'source': "reddit"} for post in reddit_api_data["data"]["children"]]
                        
                        for index,item in enumerate(reddit_api_res):
                            news_article = NewsArticle.objects.filter(query = query, id=expired_news.data[index]["article"], source="reddit").update(headline = item["headline"], link= item["link"], source= item["source"])
                            UserArticle.objects.filter(article_id=expired_news.data[index]["article"]).update(created_at=datetime.now(pytz.timezone('UTC')))
    
                        return Response(reddit_api_res, status=status.HTTP_200_OK)
            
                    elif news_api_response.status_code == 200:
                        news_api_data = news_api_response.json()
                        news_api_res = [{'headline': article["title"], 'link': article["url"], 'source': "newsapi"} for article in news_api_data["articles"]]
                        
                        for index,item in enumerate(news_api_res):
                            news_article = NewsArticle.objects.filter(query = query, id=expired_news.data[index]["article"], source="newsapi").update(headline = item["headline"], link= item["link"], source= item["source"])
                            UserArticle.objects.filter(article_id=expired_news.data[index]["article"]).update(created_at=datetime.now(pytz.timezone('UTC')))
                        
                        return Response(news_api_res, status=status.HTTP_200_OK)

                    else:
                        return Response({'error': 'Unable to retrieve news from any source.'}, status=status.HTTP_404_NOT_FOUND)
                
                
                print('not expired')
                valid_articles = NewsArticleSerializer(NewsArticle.objects.filter(query=query, user=request.user), many=True)
                valid_articles = [{'headline' : v_article['headline'], 'link' : v_article['link'], 'source' : v_article['source']} for v_article in valid_articles.data]
                return Response(valid_articles, status=status.HTTP_200_OK)
            
            
            print('create fresh records')
            if reddit_api_response.status_code == 200 and news_api_response.status_code == 200:
                reddit_api_data = reddit_api_response.json()
                news_api_data = news_api_response.json()
                reddit_api_res = [{'headline': post["data"]["title"], 'link': post["data"]["url"], 'source': "reddit"} for post in reddit_api_data["data"]["children"]]
                news_api_res = [{'headline': article["title"], 'link': article["url"], 'source': "newsapi"} for article in news_api_data["articles"]]
                combined_news = news_api_res + reddit_api_res
                for i in combined_news:
                    news_article = NewsArticle(query = query, headline = i["headline"], link= i["link"], source= i["source"], user=request.user)
                    user_article = UserArticle(user=request.user,article=news_article, query=query)
                    news_article.save()
                    user_article.save()
                return Response((news_api_res + reddit_api_res), status=status.HTTP_200_OK)
            
            elif reddit_api_response.status_code == 200:
                reddit_api_data = reddit_api_response.json()
                reddit_api_res = [{'headline': post["data"]["title"], 'link': post["data"]["url"], 'source': "reddit"} for post in reddit_api_data["data"]["children"]]
                for i in reddit_api_res:
                    news_article = NewsArticle(query = query, headline = i["headline"], link= i["link"], source= i["source"],user=request.user)
                    user_article = UserArticle(user=request.user,article=news_article,query=query)
                    news_article.save()
                    user_article.save()
                return Response(reddit_api_res, status=status.HTTP_200_OK)
            
            elif news_api_response.status_code == 200:
                news_api_data = news_api_response.json()
                news_api_res = [{'headline': article["title"], 'link': article["url"], 'source': "newsapi"} for article in news_api_data["articles"]]
                for i in news_api_res:
                    news_article = NewsArticle(query = query, headline = i["headline"], link= i["link"], source= i["source"],user=request.user)
                    user_article = UserArticle(user=request.user,article=news_article,query=query)
                    news_article.save()
                    user_article.save()
                return Response(news_api_res, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Unable to retrieve news from any source.'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#-------------------------------------------------------------------------------------------------------------------------------------------------------    

#-----------------Fetch General News (/news)----------------------------------------------------------------------------------------------------------   
    else:
        try:
            reddit_api_response= get_reddit_api_data()
            news_api_response= get_news_api_data()

            if reddit_api_response.status_code == 200 and news_api_response.status_code == 200:
                reddit_api_data = reddit_api_response.json()
                news_api_data = news_api_response.json()
                reddit_api_res = [{'headline': post["data"]["title"], 'link': post["data"]["url"], 'source': "reddit"} for post in reddit_api_data["data"]["children"]]
                news_api_res = [{'headline': article["title"], 'link': article["url"], 'source': "newsapi"} for article in news_api_data["articles"]]
                return Response((news_api_res + reddit_api_res), status=status.HTTP_200_OK)
            
            elif reddit_api_response.status_code == 200:
                reddit_api_data = reddit_api_response.json()
                reddit_api_res = [{'headline': post["data"]["title"], 'link': post["data"]["url"], 'source': "reddit"} for post in reddit_api_data["data"]["children"]]
                return Response(reddit_api_res, status=status.HTTP_200_OK)
            
            elif news_api_response.status_code == 200:
                news_api_data = news_api_response.json()
                news_api_res = [{'headline': article["title"], 'link': article["url"], 'source': "newsapi"} for article in news_api_data["articles"]]
                return Response(news_api_res, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Unable to retrieve news from any source.'}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#----------------------------------------------------------------------------------------------------------------------------------------------------    

@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def process_favorite_news(request):
#--------------------------Mark User Articles as Favorite or vice versa ( /news/favourite?user= &id= )------------------------------------------------
    if request.method == 'POST':
        try:
            if 'user' not in request.GET or 'id' not in request.GET:
                return Response({'error' : 'Invalid request parameter'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = request.GET.get('user')
            id = request.GET.get('id')

            user_article = UserArticle.objects.filter(user=user, article_id=id).first()
            if user_article:
                news_article = NewsArticle.objects.filter(id=user_article.article_id).first()

                if user_article.favorite == True:
                    user_article.favorite = False
                else:
                    user_article.favorite = True

                user_article.updated_at = datetime.now(pytz.timezone('UTC'))
                user_article.save()
                return Response({
                        "user" : user,
                        "favorite" : user_article.favorite,
                        "id" : int(id),
                        "headline" : news_article.headline,
                        "link" : news_article.link,
                        "source" : news_article.source
                    }, status=status.HTTP_200_OK)
            
            return Response({"error" : "user or article not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#------------------------------------------------------------------------------------------------------------------------------------------------   

#---------------------------------------Get most recently favourited articles of user ( /news/favourite?user= )----------------------------------------
    elif request.method == 'GET':
        try:
            if 'user' not in request.GET:
                return Response({'error' : 'Invalid request parameter'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = request.GET.get('user')
            recent_favs = UserArticleSerializer(UserArticle.objects.filter(user=user, favorite=True).order_by('-updated_at'), many=True).data
            
            if len(recent_favs) > 0:
                result = []
                for favs in recent_favs:
                    fav_article_data = NewsArticleSerializer(NewsArticle.objects.filter(id=favs["article"]).first()).data
                    result.append({
                        "id" : favs["article"],
                        "headline" : fav_article_data["headline"],
                        "link" : fav_article_data["link"],
                        "source" : fav_article_data["source"]
                    })
                
                return Response(result, status=status.HTTP_200_OK)

            return Response({"error" : "No Favorite articles found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#--------------------------------------------------------------------------------------------------------------------------------------------------