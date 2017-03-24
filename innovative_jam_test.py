# -*- coding: utf-8 -*-
import time
import sys
import tweepy
from account_settings import *
from jam_recipe import *
from kitchen.text.converters import getwriter
from random import randrange

# Innovative Jam Test run
# Use this file to print test runs to stdout
if __name__ =='__main__':
    # enable unicode in stdout
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
        return get_full_tweet(jname)
       

    while True:
        print make_jam()
        time.sleep(5)




    
