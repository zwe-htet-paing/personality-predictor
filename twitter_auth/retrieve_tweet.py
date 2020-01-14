import csv
from datetime import datetime
import os
import re
import requests
import twitter
import lxml.html
import pandas as pd

TWITTER_CONS_KEY = 'uhzOXpxETxaIXRKFmG4J10ztP'
TWITTER_CONS_SEC = 'SZBltYRGECF2pJ6t4PMqtRYRGReEFHVam2jxZa97xkJnyiSCki'
TWITTER_ACCESS_TOKEN = '1121670465838178304-4MmnwoM6bWS53X7hJwdij5Vsb09emC'
TWITTER_ACCESS_SEC = 'BEIZVVAyRNS3kkeeR37ZwyuZ0j2F1uxNV8dAQZTqlK9h2'

t = twitter.Api(
    consumer_key = TWITTER_CONS_KEY,
    consumer_secret = TWITTER_CONS_SEC,
    access_token_key = TWITTER_ACCESS_TOKEN,
    access_token_secret = TWITTER_ACCESS_SEC,
    tweet_mode='extended' # this ensures that we get the full text of the users' original tweets
)


def get_tweets(first_200, screen_name, last_id):
    all_tweets = []
    all_tweets.extend(first_200)
    for i in range(900):
        new = t.GetUserTimeline(screen_name=screen_name, max_id=last_id-1)
        if len(new) > 0:
            all_tweets.extend(new)
            last_id = new[-1].id
        else:
            break

    return all_tweets




def write_to_csv(tweets, filename):
    headers = ['id','full_text','source']

    with open('twitter_auth/users/'+filename + '.csv', 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(headers)

        for item in tweets:
            writer.writerow([item.id,
                             item.full_text,

                             clean_source(item.source)])
    csvfile.close()

def clean_source(source):
    """
    Turns data including the source and some html like this -
    <a href="https://www.sprinklr.com" rel="nofollow">Sprinklr</a> - to a list like this -
    ['Sprinklr']
    """
    raw = lxml.html.document_fromstring(source)
    return raw.cssselect('body')[0].text_content()



def get_user_tweet(name):

    screen_name = name

    first_200 = t.GetUserTimeline(screen_name=screen_name, count=200)

    all_tweets = get_tweets(first_200, screen_name, first_200[-1].id)
    #write_to_csv(all_tweets , screen_name + '_tweets')

    return all_tweets
