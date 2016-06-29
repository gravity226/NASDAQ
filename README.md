# Market Pulse
 - This project uses sentiment analysis from Twitter tweets to help make predictions on the stock market.  Every tweet used is associated to a particular stock symbol when a #(stock symbol) is found.  For example, the #SP500 is assumed to be related to the SP 500 stock.  

### Table Of Contents
 - [Gathering Tweets](https://github.com/gravity226/NASDAQ#gathering-tweets)


### Gathering Tweets
<img src="https://raw.githubusercontent.com/gravity226/NASDAQ/master/imgs/twitter_to_mongo.tiff" />
Tweets were gathered using the [Tweepy](http://www.tweepy.org/) Python library.  Tweets were streamed in real time and saved to a MongoDB database.  Anywhere from 4-6 million tweets were gathered per day.

See [save_stock_tweets.py](https://github.com/gravity226/NASDAQ/blob/master/testing/save_stock_tweets.py) for the code.
