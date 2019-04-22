#!/usr/bin/env python
# coding: utf-8

# In[12]:


import sys

sys.path.append("../")  # go to parent dir

# In[32]:


import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
from accessconfig import *
import json
import boto3
import logging
import re
import time
from twitter_rest_producer import tweetParser, sendToFirehose

# 1. Create a class inheriting from StreamListener
# 2. Using that class create a Stream object
# 3. Connect to the Twitter API using the Stream.

# In[33]:


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)


# In[39]:


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
        print(find_title)
        jobpost["job_title"] = ' '.join(find_title)

        if find_skills or find_skills_htag:
            jobpost["technologies"] = ','.join(find_skills or find_skills_htag)

        if find_city or find_city_htag or place or coordinates:
            jobpost["city"] = ','.join(find_city or find_city_htag) or place or coordinates

        if find_type or find_type_htag:
            jobpost["job_type"] = ','.join(find_type or find_type_htag)

        if urls:
            jobpost["links"] = ', '.join(urls)
        print(jobpost)
        print("------------------------------------------------")
        return jobpost
    else:
        return None


# In[42]:


class TweeterStreamListener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = tweetParser(all_data)
        try:
            jobpost = makeJobpost(tweet)
        #             if jobpost:
        #                 sendToFirehose(jobpost)
        except tweepy.TweepError as e:
            self.log.error("Error when sending tweet: %s" % e)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False


# In[41]:

def startStreaming():
    runtime = 600  # Tracking for 600  seconds
    twitterStream = Stream(auth, TweeterStreamListener())
    twitterStream.filter(languages=["en"], track=['hiring', 'hire', 'looking for', 'job'], async=True)
    time.sleep(runtime)
    twitterStream.disconnect()

