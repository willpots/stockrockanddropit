from news import TwitterNews

twitter = TwitterNews('Resources/articles.db')
# Twitter usernames & keywords
# hardcore hardcoding of query tuples [('SYMBOL', ['KEYWORDS', ...], ['USERNAMES', ...]), ...]
query_tuples = [('AAPL', [], []), ('GOOG', [], []),('NFLX', [], []),('TSLA', ['Tesla Motors'], []),('FB', [], [])]
twitter.scrape_wrapper(query_tuples, 2)