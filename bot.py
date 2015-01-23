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
import random
import json
#from replies import replies_list


class StdOutListener(tweepy.streaming.StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    last_own_tweet = None

    def on_data(self, data):
        data = json.loads(data)
        try:
            # FIXME: how to test if already faved?
            api.create_favorite(data.get('id'))
        except:
            pass

        # FIXME: analyse here

        # FIXME: reply
        api.update_status(
            status='@%s FIXME' % (data.get('user').get('screen_name')),
            in_reply_to_status_id=data.get('id'))
        return True

    def on_error(self, status):
        print(status)


l = StdOutListener()
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(CLIENT_TOKEN, CLIENT_SECRET)
api = tweepy.API(auth)

stream = tweepy.Stream(auth, l)
stream.filter(follow=USER_LIST)
