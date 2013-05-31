#! /usr/bin/env python

#from news import TwitterNews
# twitter = TwitterNews('Resources/articles.db')
# Twitter usernames & keywords
# hardcore hardcoding of query tuples [('SYMBOL', ['KEYWORDS', ...], ['USERNAMES', ...]), ...]
#query_tuples = [('AAPL', [], []), ('GOOG', [], []),('NFLX', [], []),('TSLA', ['Tesla Motors'], []),('FB', [], [])]
#twitter.scrape_wrapper(query_tuples, 2)

from feed_archiver import FeedArchiver as FA

feeds = [	'https://www.google.com/finance/company_news?q=NASDAQ:AAPL&ei=bmGmUdDhOOWu0AGvPw&output=rss',
			'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml' ]

feedArchiver = FA('articles.db', feeds)
feedArchiver.check_all()