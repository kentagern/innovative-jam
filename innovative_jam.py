# -*- coding: utf-8 -*-
import time
import sys
import tweepy
from account_settings import *
from jam_recipe import *
from kitchen.text.converters import getwriter

UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
 
# set up Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

set_up_vars()



def make_jam():
    jingr = get_ingredient()
    jname = get_jam_name(jingr)
    jstring = get_full_tweet(jname)
    
    print jstring


make_jam()

#api.update_status(tstring)
i = 0
while i < 100:
    make_jam()
    
    i = i + 1
    time.sleep(1)




