import tweepy
from tweepy import OAuthHandler
from accessconfig import *
import json
import boto3
import logging
from routes import build_message


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

query = """-senior -frontend -staff -principal -contract -lead
          "data engineer" OR "data scientist" OR "software engineer" OR "software developer" OR "backend engineer" OR "python developer" OR flask
          (hiring OR "looking for" OR opening OR job)"""


def tweetParser(tweet):
    selected = {
                "created_at": tweet["created_at"],
                "text": tweet["text"],
                "user_name": tweet["user"]["name"],
                "user_description": tweet["user"]["description"],
                "place": tweet["place"]["full_name"] if tweet["place"] else None,
                "coordinates": tweet["coordinates"]["coordinates"] if tweet["coordinates"] else None,
                "hashtags": [hashtag["text"] for hashtag in tweet["entities"]["hashtags"]],
                "urls": [url["expanded_url"] for url in tweet["entities"]["urls"]],
               }

    return selected


def run():
 try:
     results = tweepy.Cursor(api.search, q=query, lang="en", geocode="40.730610,-73.935242,40.0mi").items(500)
     for tweet in results:
        tweet = json.dumps(tweetParser(tweet._json))
        print(tweet)
        sendToFirehose(tweet)
 except tweepy.TweepError as e:
     print(e.response)



firehose = boto3.client('firehose', region_name='us-east-1')
LOG_FILENAME = '../logs/stream_producer_log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def sendToFirehose(tweet):
    try:
        response = firehose.put_record(DeliveryStreamName="twitter-data-stream",
                                       Record={
                                           'Data': tweet + ',\n'
                                       })
        logging.info(response)
    except Exception as err:
        logging.exception(build_message("Error encountered while pushing to Firehose", err))


if __name__ == '__main__':
    # while True:
    run()
        #every 3 minutes
    # time.sleep(180)

