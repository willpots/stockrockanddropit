import feedparser as fp
import cpickle as pickle
from urlparse import urlsplit
import diffbot
class FeedArchiver(object):

	class Feed(object):
		def __init__(self, name, url, etag=None, modified=None):
			self.name = name
			self.url = url
			self.etag = etag
			self.modified = modified

	def __init__(self, feeds=[]):
		self.feeds = feeds
		self.diff = DiffBot('2da7b7ab395d266525483f6f30d3758e')
		self.conn = False

	def load(self, filename):
		pickle.dump(self.feeds, open(filename, 'w+'))

	def save(self, filename):
		self.feeds = pickle.load(open(filename, 'r'))

	def get_feed(self, feed):
		if feed.etag
			parser = fp.parse(feed.url, etag=feed.etag)
			feed.etag = parser.etag
		elif feed.modified:
			parser = fp.parse(feed.url, modified=feed.modified)
			feed.modified = parser.modified
		else:
			parser = fp.parse(feed.url)
			feed.etag = parser.etag
			feed.modified = parser.modified
		docs = []
		for f in parser.feeds:
			doc = self.diff(url)
			doc_tuple = (doc.date, urlsplit(doc.url)[1], doc.title, doc.text, doc.url)
			docs.append(docs)


	def check_all(self):
		reduce(lambda a,b: a+b, map(self.get_feed, self.feeds))

	def db_open(self):
		self.conn = sqlite3.connect(self.db_name)

	def db_close(self):
		self.conn.close()
		self.conn = False

	def db_create(self):
		if not self.conn:
			self.db_open()
		c = self.conn.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS articles (date text, domain text, title text, body text, url text, UNIQUE (url))''')
		self.conn.commit()

	def db_insert(self, articles):
		if not self.conn:
			self.db_open()
			c = self.conn.cursor()
		c.executemany('INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?, ?, ?)', articles)
		self.conn.commit()
