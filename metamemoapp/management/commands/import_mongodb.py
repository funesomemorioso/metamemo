from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from metamemoapp.models import MetaMemo, MemoItem, MemoSource, MetaScraper
from bson import Binary, Code
from bson.json_util import dumps
import datetime

# import csv
import json
import pymongo



class Command(BaseCommand):
    
    help = 'MongoDB'

    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client["smdata"]
    
    col_posts_facebook = db["posts_facebook"]  
    col_posts_twitter = db["posts_twitter"]  
    col_posts_instagram = db["posts_instagram"] 

    i_fb = 0
    i_in = 0
    i_tw = 0

    bln_qtd_test = False
    int_qtd_test = 50
    int_qtd_test = int_qtd_test-1 # =p


    

    def handle(self, *args, **kwargs):
        
        
        t1 = datetime.datetime.now()
        
        
        

        self.get_accounts()

        t2 = datetime.datetime.now()
        

        print(t1)
        print(t2)
        print(t2-t1)

        print("POSTs FACEBOOK #:"+str(self.i_fb))
        print("POSTs TWITTER #:"+str(self.i_tw))
        print("POSTs INSTAGRAM #:"+str(self.i_in))

        print("POSTs TOTAL #:"+str(self.i_fb+self.i_tw+self.i_in))



     
    def get_accounts(self):
        
        accounts = [

            {
                "name": "Jair Bolsonaro",
                "acc": "jairmessias.bolsonaro",
                "acc_facebook": "jairmessias.bolsonaro",
                "acc_twitter": "jairbolsonaro",
                "acc_instagram": "jairmessiasbolsonaro"
 
 
            },

            {
                "name": "Carlos Bolsonaro",
                "acc": "cbolsonaro",
                "acc_facebook": "cbolsonaro",
                "acc_twitter": "CarlosBolsonaro",
                "acc_instagram": "carlosbolsonaro"
            },

            {
                "name": "Flavio Bolsonaro",
                "acc": "flaviobolsonaro",
                "acc_facebook": "flaviobolsonaro",
                "acc_twitter": "FlavioBolsonaro",
                "acc_instagram": "flaviobolsonaro"
            },

            {
                "name": "Renan Bolsonaro",
                "acc": "JairRenan.Bolsonaro",
                "acc_facebook": "JairRenan.Bolsonaro",
                "acc_twitter": "renan_bolsonaro",
                "acc_instagram": "bolsonaro_jr"
            }
        ] 

        for account in accounts:
            self.import_target_facebook_data(account["acc_facebook"], account["name"])
            self.import_target_twitter_data(account["acc_twitter"], account["name"])
            self.import_target_instagram_data(account["acc_instagram"], account["name"])

    def import_target_facebook_data(self, str_target_account, str_name):
        print(str_target_account)

        # ====================== FACEBOOK =======================
        
        c = self.col_posts_facebook.find( { "user_url": { "$regex": '.*'+str_target_account+'.*' }} )
        i = 0
        
        for post in c:
            if(self.bln_qtd_test and self.i_fb>self.int_qtd_test): break
            self.i_fb = self.i_fb + 1
            
            print("POST FACEBOOK #:"+str(i))
            
            memo_item = MemoItem()
            
            str_post_date  =  '1981-01-24 00:00:00',
            if('time' in post):
               str_post_date = str(post['time'])

            str_text  =  'None',
            if('text' in post):
               str_text = str(post['text'])

            str_post_text  =  'None',
            if('post_text' in post):
               str_post_text = str(post['post_text'])

            print(str_post_date) 
        

            memo_author = MetaMemo.objects.get_or_create(name=str_name)
            memo_source = MemoSource.objects.get_or_create(name='FB '+str_name)
            
            memo_item.author = memo_author[0]
            memo_item.source = memo_source[0]
            
            
            memo_item.title = str_text[0:139]
            memo_item.content = str_post_text
            memo_item.extraction_date = '2022-01-24 00:00:00'
            memo_item.content_date =   str_post_date
            # memo_item.content_date = post['time']
            memo_item.url = post['post_url']
            memo_item.likes = post['likes']
            memo_item.interactions = post['comments']
            memo_item.raw = str(post)
            memo_item.save()

            
            i = i+1

    
    def import_target_twitter_data(self, str_target_account, str_name):
        print(str_target_account)

        # ====================== TWITTER =======================
        
        c = self.col_posts_twitter.find( { "user.username": { "$regex": '.*'+str_target_account+'.*' }} )
        i = 0
        
        for post in c:
            if(self.bln_qtd_test and self.i_tw>self.int_qtd_test): break
            self.i_tw = self.i_tw + 1
            print("POST TWITTER #:"+str(i))
            
    
            memo_item = MemoItem()
            str_post_date  =  '1981-01-24 00:00:00',
            if('date' in post):
               str_post_date = str(post['date'])

            print(str_post_date)

            memo_author = MetaMemo.objects.get_or_create(name=str_name)
            memo_source = MemoSource.objects.get_or_create(name='TW '+str_name)
            
            memo_item.author = memo_author[0]
            memo_item.source = memo_source[0]
            
            memo_item.followers = post['user']['followersCount']
            
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

    
    def import_target_instagram_data(self, str_target_account, str_name):
        print(str_target_account)

        # ====================== INSTAGRAM =======================
        
        c = self.col_posts_instagram.find( { "account.handle": { "$regex": '.*'+str_target_account+'.*' }} )
        i = 0
        
        for post in c:
            if(self.bln_qtd_test and self.i_in>self.int_qtd_test): break
            self.i_in = self.i_in + 1
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
            

            memo_author = MetaMemo.objects.get_or_create(name=str_name)
            memo_source = MemoSource.objects.get_or_create(name='IN '+str_name)
            
            memo_item.author = memo_author[0]
            memo_item.source = memo_source[0]
            
            memo_item.followers = post['account']['subscriberCount']

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
            
