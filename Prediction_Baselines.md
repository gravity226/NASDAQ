# Second Attempt - "The Featuring"
## RandomForestClassifier



```python

```

# First Attempt
## RandomForestClassifier

Accuracy Score: 0.704918032787
Working with one stock sym, 'goog'.

```python
  from yahoo_finance import Share
  import pandas as pd
  from sklearn.metrics import accuracy_score
  from sklearn.ensemble import RandomForestClassifier

  sym = 'goog'
  yahoo = Share(sym)

  historical_train = yahoo.get_historical('2010-01-01', '2016-01-01')
  historical_test = yahoo.get_historical('2016-01-02', '2016-04-03')

  for n in xrange(1, len(historical_train)-1):
      if historical_train[n+1]['Close'] > historical_train[n]['Close']:
          historical_train[n]['Pred'] = 'above'
      elif historical_train[n+1]['Close'] < historical_train[n]['Close']:
          historical_train[n]['Pred'] = 'below'
      else:
          historical_train[n]['Pred'] = 'equal'
      #print historical[n]['Pred']

  for n in xrange(1, len(historical_test)-1):
      if historical_test[n+1]['Close'] > historical_test[n]['Close']:
          historical_test[n]['Pred'] = 'above'
      elif historical_test[n+1]['Close'] < historical_test[n]['Close']:
          historical_test[n]['Pred'] = 'below'
      else:
          historical_test[n]['Pred'] = 'equal'

  #historical.pop()
  df_train = pd.DataFrame(historical_train[1:len(historical_train)])
```
