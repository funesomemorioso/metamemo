from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from metamemoapp.models import MetaMemo, MemoItem, MemoSource, MetaScraper
from bson import Binary, Code
from bson.json_util import dumps

# import csv
import json
import pymongo



class Command(BaseCommand):
    
    help = 'MongoDB'
    
    

    # def add_arguments(self, parser):
    #     parser.add_argument('-f', '--filename', type=str, help='CSV File to be imported')
    #     parser.add_argument('-a', '--author', type=str, help='MetaMemo Author Name')


    def handle(self, *args, **kwargs):
        # filename = kwargs['filename']
        # author = kwargs['author']
        
        # memo_author = MetaMemo.objects.get_or_create(name=author)
        # memo_source = MemoSource.objects.get_or_create(name='Facebook')

        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        db = client["smdata"]
        col_posts_facebook = db["posts_facebook"]  
        col_posts_twitter = db["posts_twitter"]  
        col_posts_instagram = db["posts_instagram"]  

        # post.objects.bulk_create() <-- não rolou
        # with transaction.atomic(): <-- nem esse


#         {
#   "_id": {
#     "$oid": "6202c480e980dfe6bbe1fb2a"
#   },
#   "_type": "snscrape.modules.twitter.Tweet",
#   "cashtags": null,
#   "content": "- Camilla começou a estudar química e produzir seus próprios métodos de tratamento. A busca por conhecimento deu resultados, tanto em aparência quanto em conhecimento: enquanto estudava, a jovem descobriu a astroquímica, ramo da ciência que trata da evolução química do universo.",
#   "conversationId": 1463077533826617300,
#   "coordinates": null,
#   "date": "2021-11-23T09:31:14+00:00",
#   "hashtags": null,
#   "id": 1463077670816817200,
#   "inReplyToTweetId": 1463077533826617300,
#   "inReplyToUser": {
#     "_type": "snscrape.modules.twitter.User",
#     "created": "2010-03-31T23:13:44+00:00",
#     "description": "Capitão do Exército Brasileiro, eleito 38° Presidente da República Federativa do Brasil. 🇧🇷.",
#     "descriptionUrls": null,
#     "displayname": "Jair M. Bolsonaro",
#     "favouritesCount": 4740,
#     "followersCount": 7178919,
#     "friendsCount": 532,
#     "id": 128372940,
#     "label": null,
#     "linkTcourl": "https://t.co/DzletgH0tv",
#     "linkUrl": "https://t.me/jairbolsonarobrasil",
#     "listedCount": 7479,
#     "location": "Brasília, Brasil",
#     "mediaCount": 5371,
#     "profileBannerUrl": "https://pbs.twimg.com/profile_banners/128372940/1540929521",
#     "profileImageUrl": "https://pbs.twimg.com/profile_images/1057631480459886595/9VPdGJJz_normal.jpg",
#     "protected": false,
#     "rawDescription": "Capitão do Exército Brasileiro, eleito 38° Presidente da República Federativa do Brasil. 🇧🇷.",
#     "statusesCount": 12839,
#     "url": "https://twitter.com/jairbolsonaro",
#     "username": "jairbolsonaro",
#     "verified": true
#   },
#   "lang": "pt",
#   "likeCount": 10072,
#   "media": null,
#   "mentionedUsers": null,
#   "outlinks": null,
#   "place": null,
#   "quoteCount": 10,
#   "quotedTweet": null,
#   "renderedContent": "- Camilla começou a estudar química e produzir seus próprios métodos de tratamento. A busca por conhecimento deu resultados, tanto em aparência quanto em conhecimento: enquanto estudava, a jovem descobriu a astroquímica, ramo da ciência que trata da evolução química do universo.",
#   "replyCount": 109,
#   "retweetCount": 1390,
#   "retweetedTweet": null,
#   "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
#   "sourceLabel": "Twitter for iPhone",
#   "sourceUrl": "http://twitter.com/download/iphone",
#   "tcooutlinks": null,
#   "url": "https://twitter.com/jairbolsonaro/status/1463077670816817152",
#   "user": {
#     "_type": "snscrape.modules.twitter.User",
#     "created": "2010-03-31T23:13:44+00:00",
#     "description": "Capitão do Exército Brasileiro, eleito 38° Presidente da República Federativa do Brasil. 🇧🇷.",
#     "descriptionUrls": null,
#     "displayname": "Jair M. Bolsonaro",
#     "favouritesCount": 4740,
#     "followersCount": 7178919,
#     "friendsCount": 532,
#     "id": 128372940,
#     "label": null,
#     "linkTcourl": "https://t.co/DzletgH0tv",
#     "linkUrl": "https://t.me/jairbolsonarobrasil",
#     "listedCount": 7479,
#     "location": "Brasília, Brasil",
#     "mediaCount": 5371,
#     "profileBannerUrl": "https://pbs.twimg.com/profile_banners/128372940/1540929521",
#     "profileImageUrl": "https://pbs.twimg.com/profile_images/1057631480459886595/9VPdGJJz_normal.jpg",
#     "protected": false,
#     "rawDescription": "Capitão do Exército Brasileiro, eleito 38° Presidente da República Federativa do Brasil. 🇧🇷.",
#     "statusesCount": 12839,
#     "url": "https://twitter.com/jairbolsonaro",
#     "username": "jairbolsonaro",
#     "verified": true
#   }
# }
        
        # ====================== TWITTER =======================
        
        c = col_posts_twitter.find({})
        i = 0
        for post in c:
            print("POST TWITTER #:"+str(i))
            print(str(post['date']))
    
            memo_item = MemoItem()
            str_post_date  =  '1981-01-24 00:00:00',
            if('date' in post):
               str_post_date = str(post['date'])
        

            memo_author = MetaMemo.objects.get_or_create(name=post['user']['displayname'])
            memo_source = MemoSource.objects.get_or_create(name='Twitter')
            
            memo_item.author = memo_author[0]
            memo_item.source = memo_source[0]
            
            
            memo_item.title = post['content'][0:139]
            memo_item.content = post['content']
            memo_item.extraction_date = '2022-01-24 00:00:00'
            memo_item.content_date = str_post_date
            # memo_item.content_date = post['time']
            memo_item.url = post['url']
            memo_item.likes = post['likeCount']
            memo_item.interactions = post['replyCount']
            memo_item.raw = str(post)
            memo_item.save()

            
            i = i+1





        # ====================== FACEBOOK =======================
        
        c = col_posts_facebook.find({})
        i = 0
        for post in c:
            print("POST FACEBOOK #:"+str(i))
            print(str(post['time']))
    
            memo_item = MemoItem()
            str_post_date  =  '1981-01-24 00:00:00',
            if('time' in post):
               str_post_date = str(post['time'])
        

            memo_author = MetaMemo.objects.get_or_create(name=post['username'])
            memo_source = MemoSource.objects.get_or_create(name='Facebook')
            
            memo_item.author = memo_author[0]
            memo_item.source = memo_source[0]
            
            
            memo_item.title = post['text'][0:139]
            memo_item.content = post['post_text']
            memo_item.extraction_date = '2022-01-24 00:00:00'
            memo_item.content_date =   str_post_date
            # memo_item.content_date = post['time']
            memo_item.url = post['post_url']
            memo_item.likes = post['likes']
            memo_item.interactions = post['comments']
            memo_item.raw = str(post)
            memo_item.save()

            
            i = i+1





        
        # ====================== INSTAGRAM =======================
        
        c = col_posts_instagram.find({})
        i = 0
        for post in c:
            print("POST INSTAGRAM #:"+str(i))
            print(str(post['date']))
    
            memo_item = MemoItem()
            str_post_date  =  '1981-01-24 00:00:00',
            if(post['date']!=None):
               str_post_date = str(post['date'])
            
            str_descritpion  =  'None',
            if("description" in post):
                str_descritpion = post['description']
            
            str_post_url  =  'None',
            if("postUrl" in post):
                str_post_url = post['postUrl']
            

            memo_author = MetaMemo.objects.get_or_create(name=post['account']['handle'])
            memo_source = MemoSource.objects.get_or_create(name='Instagram')
            
            memo_item.author = memo_author[0]
            memo_item.source = memo_source[0]
            
            
            memo_item.title = str_descritpion
            memo_item.content = post['media'][0]['url']
            memo_item.extraction_date = '2022-01-24 00:00:00'
            memo_item.content_date =    str_post_date
            memo_item.url = str_post_url
            memo_item.likes = post['statistics']['actual']['favoriteCount']
            memo_item.interactions = post['statistics']['actual']['commentCount']
            memo_item.raw = str(post)
             #memo_item.medias = MemoMedia
            memo_item.save()

            
            i = i+1
            
    


