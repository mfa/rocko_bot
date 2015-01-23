# -*- coding: utf-8 -*-

# set credentials in credentials.py
from credentials import (
    API_KEY,
    API_SECRET,
    CLIENT_TOKEN,
    CLIENT_SECRET,
    # user_list as ids (strings)
    USER_LIST,
)

import tweepy
from tweepy.error import TweepError
import random
import json
from replies import replies_dict, nothing_found
from nltk.stem.snowball import GermanStemmer


auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(CLIENT_TOKEN, CLIENT_SECRET)
api = tweepy.API(auth)


def generate_status(username, text):
    found = []
    stemmer = GermanStemmer()
    key_mapper = []
    stemmed_keys = []
    for key in replies_dict.keys():
        key_mapper.append((key, stemmer.stem(key)))
        stemmed_keys.append(stemmer.stem(key))
    for word in text.split(' '):
        if stemmer.stem(word) in stemmed_keys:
            found.append(dict(key_mapper).get(word))
    if found:
        status = u'@%s %s' % (
            username,
            random.choice(replies_dict.get(random.choice(found))))
    else:
        status = u'@%s %s' % (
            username,
            random.choice(nothing_found))
    return status


class StdOutListener(tweepy.streaming.StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    last_own_tweet = None

    def on_data(self, data):
        data = json.loads(data)
        username = data.get('user').get('screen_name')
        text = data.get('text')
        print(username),
        print(text)
        try:
            # FIXME: how to test if already faved?
            api.create_favorite(data.get('id'))
        except:
            pass

        status = generate_status(username, text)
        api.update_status(
            status=status,
            in_reply_to_status_id=data.get('id'))
        return True

    def on_error(self, status):
        print(status)


l = StdOutListener()

stream = tweepy.Stream(auth, l)
while True:
    try:
        stream.filter(follow=USER_LIST)
    except TweepError:
        pass
