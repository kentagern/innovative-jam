import time
import tweepy
from account_settings import *
from jam_recipe import *



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# grab main ingredient
jingr = "cherry"
jname = getJamName(jingr)

descr1 = getDescriptor()

tstring = jname + getDescriptor()

api.update_status(tstring)




