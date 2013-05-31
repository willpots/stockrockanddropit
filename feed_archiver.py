import feedparser as fp
import pickle
import json
import sqlite3
import datetime
from urlparse import urlsplit
from urllib import quote_plus as url_encode
import requests as r

DIFFBOT = 'http://www.diffbot.com/api/article?token=2da7b7ab395d266525483f6f30d3758e&url='
class FeedArchiver(object):
	def __init__(self, db_name, feeds=[]):
		''' db_name is the name of the sqlite3 db and feeds should be a list of urls #hardcodedsecret '''
		self.db_name = db_name
		self.feeds = map(lambda u: self.Feed(u), feeds)
		self.conn = False

	# main fn
	def check_all(self):
		self.db_open()
		self.db_create()
		all_articles = reduce(lambda a,b: a+b, map(self.get_feed, self.feeds))
		if all_articles:
			print "%d new articles" % len(all_articles)
			self.db_insert(all_articles)
		else:
			print "no new articles"
		self.db_close()

	# struct object, if we end up with a lot of these a named tuple might be better.
	class Feed(object):
		def __init__(self, url, title=None, etag=None, modified=None):
			self.title = title
			self.url = url
			self.etag = etag
			self.modified = modified

	# Packing/Unpacking of feed metadata
	def load(self, filename):
		pickle.dump(self.feeds, open(filename, 'w+'))

	def save(self, filename):
		self.feeds = pickle.load(open(filename, 'r'))

	def get_feed(self, feed):
		''' Read feed with feedparser '''
		if feed.etag:
			parser = fp.parse(feed.url, etag=feed.etag)
			feed.title = parser.feed.title
			feed.etag = parser.etag
		elif feed.modified:
			parser = fp.parse(feed.url, modified=feed.modified)
			# if hasattr(parser.feed, 'title'):
			feed.title = parser.feed.title
			feed.modified = parser.modified
		else:
			parser = fp.parse(feed.url)
			feed.title = parser.feed.title
			if hasattr(parser, 'etag'): # assumes we only need either the etag or the modified but not both
				feed.etag = parser.etag
			elif hasattr(parser, 'modified'):
				feed.modified = parser.modified
		
		articles = []
		for f in parser.entries:
			if not self.db_url_exists(f.link):
				article = r.get(DIFFBOT+url_encode(f.link)).json()
				# figure out date
				if 'date' in article and len(article['date'].split()[0]) == 3: # the second condition checks for an abbreviated weekday name first
					date = datetime.datetime.strptime(article['date'], '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d') # may need captial %b
				else:
					date = datetime.datetime.now().strftime("%Y-%m-%d")

				# figure out url
				if 'resolved_url' in article:
					url = article['resolved_url']
				else:
					url = article['url']
				article_tuple = (date, urlsplit(url)[1], article['title'], article['text'], url)
				articles.append(article_tuple)
		return articles

	# Database stuff
	def db_open(self):
		if not self.conn:
			self.conn = sqlite3.connect(self.db_name)

	def db_close(self):
		self.conn.close()
		self.conn = False

	def db_create(self):
		''' only creates table if it doesn't exist. Hardcoded db structure '''
		c = self.conn.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS articles (date text, domain text, title text, body text, url text, UNIQUE (url))''')
		self.conn.commit()

	def db_url_exists(self, url):
		c = self.conn.cursor()
		exists = bool(c.execute('''SELECT EXISTS(SELECT 1 FROM articles WHERE url=? LIMIT 1);''', (url,)).next()[0])
		return exists

	def db_articles(self, date=None):
		c = self.conn.cursor()
		if date:
			date_str = date.strftime('%Y-%m-%d')
			return list(c.execute('SELECT title FROM articles WHERE AND date=?', (date_str,)))
		else:
			return list(c.execute('SELECT * FROM articles')) # dump database into memory yo

	def db_insert(self, articles):
		c = self.conn.cursor()
		c.executemany('INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?)', articles)
		self.conn.commit()
