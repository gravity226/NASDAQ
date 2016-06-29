# Market Pulse
 - This project uses sentiment analysis from Twitter tweets to help make predictions on the stock market.  Every tweet used is associated to a particular stock symbol when a #(stock symbol) or $(stock symbol) is found.  For example, the #SP500 or $SP500 is assumed to be related to the SP 500 stock.  

### Table Of Contents
 - [Gathering Tweets](https://github.com/gravity226/NASDAQ#gathering-tweets)
 - [Streaming Stock Quotes](https://github.com/gravity226/NASDAQ#streaming-stock-quotes)
 - [Exploratory Data Analysis](https://github.com/gravity226/NASDAQ#exploratory-data-analysis)
 - [Modeling](https://github.com/gravity226/NASDAQ#modeling)

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

<i>First Attempt</i><br />
My first attempt at getting stock data involved scraping the NASDAQ website in real time for current and historic stock quotes.  See [scrape_nasdaq.py](https://github.com/gravity226/NASDAQ/blob/master/scrape_nasdaq.py) for the code.  I ended up not using this method because it was very time consuming to get quotes.  This made it unreasonable considering I wanted to live stream quotes in a web app.  

### Exploratory Data Analysis
An easy way to get an idea of what your data is doing is to visualize it.  For this project I used [TFIDF](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) and [Nonnegative Matrix Factorization](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html) to get an easily interpretable result to graph and model.

<img src="https://github.com/gravity226/NASDAQ/blob/master/imgs/figure_1.png" width="500" />
<br />

So what does this tell me?  Well the blue line represents the closing price for a stock symbol for that day and the red lines represent the NMF values for a stock symbol for that day.  What I can see from this is that when the red lines go up then the stock market also goes up in the next day. And possibly the same is true for when the market goes down.  

See [clustering.py](https://github.com/gravity226/NASDAQ/blob/master/testing/clustering.py) for the code.

I can also get an idea of what people are saying about a particular stock symbol by looking at the most used words that relate to it.  Enter the word cloud:

<b>Word Cloud for #AAPL or Apple</b><br />
<img src="https://github.com/gravity226/NASDAQ/blob/master/testing/AAPL_wc1.png" width="500" />

<b>Word Cloud for #YHOO or Yahoo</b><br />
<img src="https://github.com/gravity226/NASDAQ/blob/master/testing/YHOO_wc1.png" width="500" />


### Modeling
To start I used a [Random Forest Classifier](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html) to see if I could simply identify whether the a particular stock symbol would increase or decrease in value in the following day.  For this approach I was getting close to %70 accuracy so I decided to move on to creating a [Random Forest Regression](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) model.  For this approach I was using the [RMSE](https://en.wikipedia.org/wiki/Root-mean-square_deviation) or Root Mean Squared Error, and the [MSE](https://en.wikipedia.org/wiki/Mean_squared_error) or Mean Squared Error to get an idea of where a stock price would close in the next day.

<img src="https://github.com/gravity226/NASDAQ/blob/master/imgs/predict.png" width="700" />
<br />

This image shows the closing prices for a weeks worth of data for the TSLA (Tesla) stock symbol.  The red box to the right of the graph shows where my model is predicting the market will fall for that day.  (You will probably notice that two points are missing here.. This is because those dates were on Saturday and Sunday and there will be no closing prices for those days.)
