#!/usr/bin/env python
# coding: utf-8

# In[12]:
from flask import jsonify, make_response

import sys

sys.path.append("../")  # go to parent dir

import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
from Data_Ingestor.accessconfig import *
import json
import re
from time import sleep
from Data_Ingestor.twitter_rest_producer import tweetParser
from random import random

# 1. Create a class inheriting from StreamListener
# 2. Using that class create a Stream object
# 3. Connect to the Twitter API using the Stream.


def retrieve_authentication():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    return auth


def makeJobpost(tweet):
    # must match
    def matchTitle(txt):
        find = re.findall(
            r"(software|data|bi|business intelligence|sales|solutions)\s?(engineer|developer|scientist|architect|consultant)",
            txt, re.IGNORECASE)
        if find:
            find = [' '.join(tp) for tp in find]
            return find
        else:
            return None

            # preferable

    def matchSkills(txt):
        find = re.findall(r"python|sql|sqlalchmey|flask|pandas|etl|aws|backend|spark|streaming|jinja", txt,
                          re.IGNORECASE)
        if find:
            return list(set(find))
        else:
            return None

            # optional

    def matchLocation(txt):
        find = re.findall(r"(new)\s?(york)|(new)\s?(jersey)|ny|nj|nyc|(jersey)\s?(city)|hoboken|brooklyn", txt,
                          re.IGNORECASE)
        if find:
            find = [' '.join(tp) for tp in find]
            return find
        else:
            return None

    # optional: even if it's not in text, it's okay
    def matchFulltime(txt):
        find = re.findall(r"full(\s|\-)?time", txt, re.IGNORECASE)
        if find:
            return find
        else:
            return None

    created_at = tweet['created_at']
    text = tweet['text']
    hashtags = ''.join(tweet['hashtags'])
    place = tweet['place']
    coordinates = tweet['coordinates']
    urls = tweet['urls']

    find_title = matchTitle(text)
    find_title_htag = matchTitle(hashtags)
    find_skills = matchSkills(text)
    find_skills_htag = matchSkills(hashtags)
    find_city = matchLocation(text)
    find_city_htag = matchLocation(hashtags)
    find_type = matchFulltime(text)
    find_type_htag = matchFulltime(hashtags)

    jobpost = {
        "city": None,
        "company": None,
        "date": None,
        "job_title": None,
        "job_type": None,
        "links": None,
        "technologies": None,
        "text": None
    }

    jobpost['text'] = text
    jobpost['date'] = created_at
    if find_title or find_title_htag:

        jobpost["job_title"] = ' '.join(find_title or find_title_htag)

        if find_skills or find_skills_htag:
            jobpost["technologies"] = ','.join(find_skills or find_skills_htag)

        if find_city or find_city_htag or place or coordinates:
            jobpost["city"] = ','.join(find_city or find_city_htag) or place or coordinates

        if find_type or find_type_htag:
            jobpost["job_type"] = ','.join(find_type or find_type_htag)

        if urls:
            jobpost["links"] = ', '.join(urls)
        return jobpost
    else:
        return None


# In[42]:


class TweeterStreamListener(StreamListener):

    def __init__(self, socketio):
        print("TweeterStreamListener is intiated")
        super().__init__()
        self.socketio = socketio

    def on_connect(self):
        print("Successfully connected to the Twitter stream")

    def on_data(self, data):
        number = round(random() * 10, 3)
        print(number)
        print("I'm getting tweets")
        all_data = json.loads(data)
        tweet = tweetParser(all_data)
        print(tweet)
        try:
            jobpost = makeJobpost(tweet)

            if jobpost:
                    # data = {"jobpost": jobpost}
                    # response = make_response(jsonify(data), 200)
                    # print(jsonify(data))
                    #return response
                    #sendToFirehose(jobpost)

                    self.socketio.emit('newtweet', {'tweet': number}, namespace='/test')


        except tweepy.TweepError as e:
            self.log.error("Error when sending tweet: %s" % e)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

class UndefinedChildClass(Exception):
    pass


class DataFlow():


    def __init__(self):
        print("initiated dataflow")
        self.auth = retrieve_authentication()


    @staticmethod
    def factory(child):
        print("factory")
        if child == 'historical':
            return HistoricalFlow()
        if child == 'live':
            return LiveFlow()

        err = 'The provided child argument (' + child + ') is not supported'
        raise UndefinedChildClass(err)



class HistoricalFlow(DataFlow):


    def __init__(self):
        print("initiated historical")
        super().__init__()
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)


    def start(self, socketio):
        query = """-senior -frontend -staff -principal -contract -lead
                  "data engineer" OR "data scientist" OR "software engineer" OR "software developer" OR "backend engineer" OR "python developer" OR flask
                  (hiring OR "looking for" OR opening OR job)"""

        try:
            print("I'm trying to get historical tweets")
            tweets = tweepy.Cursor(self.api.search, q=query, lang="en", geocode="40.730610,-73.935242,40.0mi").items(50)

            for tweet in tweets:
                tweet = tweetParser(tweet._json)
                print(tweet['text'])
                socketio.emit('newtweet', {'tweet': tweet['text']}, namespace='/test')
                sleep(2)


        except tweepy.TweepError as err:
                print(err)



    def stop(self):
        print('stop')


class LiveFlow(DataFlow):


    def __init__(self):
        print("initiated live")
        super().__init__()
        self.stream = None


    def start(self, socketio):
        listener = TweeterStreamListener(socketio)
        self.stream = tweepy.Stream(self.auth, listener)
        self.stream.filter(languages=["en"])

    def stop(self):
        self.stream.disconnect()


