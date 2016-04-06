import tweepy
import os

def get_twitter_data(sym):
    consumer_key = os.environ['TWITTER_API_KEY']
    consumer_secret = os.environ['TWITTER_SECRET_API_KEY']

    access_token = os.environ['TWITTER_API_ACCESS_TOKEN']
    access_token_secret = os.environ['TWITTER_API_ACCESS_TOKEN_SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return tweepy.Cursor(api.search, q='#' + sym.strip().upper())

if __name__ == '__main__':
    public_tweets = get_twitter_data('aapl')

    for tweet in public_tweets:
        print tweet.text




#
