import json
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

path = os.path.join(__location__, 'keys')
with open(path, "r") as read_file:
    creds = json.load(read_file)

consumer_key = creds['consumer_key']
consumer_secret = creds['consumer_secret']
access_token = creds['access_token']
access_secret = creds['access_token_secret']