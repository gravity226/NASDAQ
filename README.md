# Market Pulse
 - This project uses sentiment analysis from Twitter tweets to help make predictions on the stock market.  Every tweet used is associated to a particular stock symbol when a #(stock symbol) or $(stock symbol) is found.  For example, the #SP500 or $SP500 is assumed to be related to the SP 500 stock.  

### Table Of Contents
 - [Gathering Tweets](https://github.com/gravity226/NASDAQ#gathering-tweets)
 - [Streaming Stock Quotes](https://github.com/gravity226/NASDAQ#streaming-stock-quotes)
 - [Exploratory Data Analysis](https://github.com/gravity226/NASDAQ#exploratory-data-analysis)

### Gathering Tweets
<img src="https://github.com/gravity226/NASDAQ/blob/master/imgs/twitter_to_mongo.jpg" width="200" />
<br />
Tweets were gathered using the [Tweepy](http://www.tweepy.org/) Python library.  Tweets were streamed in real time and saved to a MongoDB database.  Anywhere from 4-6 million tweets were gathered per day.

See [save_stock_tweets.py](https://github.com/gravity226/NASDAQ/blob/master/testing/save_stock_tweets.py) for the code.

### Streaming Stock Quotes
<img src="https://github.com/gravity226/NASDAQ/blob/master/imgs/yahoo_finance.png" width="200" />
<br />
Both historical and current stock quotes were gathered via the [Yahoo Finance](https://pypi.python.org/pypi/yahoo-finance) Python library.  

See [save_stock_tweets.py](https://github.com/gravity226/NASDAQ/blob/master/stream_quotes/yahoo_quotes.py) for the code.  This includes some data cleaning and preliminary modeling.

### Exploratory Data Analysis
An easy way to get an idea of what your data is doing is to visualize it.  For this project I used [TFIDF](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) and [Nonnegative Matrix Factorization](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html) to get an easily interpretable result to graph and model.

<img src="https://github.com/gravity226/NASDAQ/blob/master/imgs/figure_1.png" width="500" />
<br />

So what does this tell me?  Well the blue line represents the closing price for a stock symbol for that day and the red lines represent the NMF values for a stock symbol for that day.  What I can see from this is that when the red lines go up then the stock market also goes up in the next day. And possibly the same is true for when the market goes down.  

See [clustering.py](https://github.com/gravity226/NASDAQ/blob/master/testing/clustering.py) for the code.
