import tweepy
from tweepy import OAuthHandler
from accessconfig import *
import json
import boto3
import logging
import time

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

query = '(New York)-(senior OR sr. OR frontend OR staff OR principal OR contract)(data engineer OR "data scientist" OR "software engineer" OR "software developer") (hiring OR "looking for" OR opening OR job OR opening)'

def main():
 for tweet in tweepy.Cursor(api.search, q=query).items(1000):
  print(tweet._json['text'])

#geocode="40.730610,-73.935242,80.0mi"
main()



