from datetime import *
import sqlite3
from random import shuffle
import ystockquote
from bs4 import BeautifulSoup
import requests
import urllib
import re

def get_current_price(symbol):
    """Pulls the current stock price from Yahoo's website by scraping"""

    symbol = symbol.lower()
    url = "http://finance.yahoo.com/q?s=" + symbol + "&ql=1"

    r = requests.get(url).text
    search = "<span id=\"yfs_l84_%s\">([0-9]+\.[0-9]+)</span>" % symbol
    price = re.search(search, r)
    price = price.group(1)
    return price


def double_shuffle(list1, list2): # shuffle two lists the same way. Used to shuffle both the labels and the docs in the dry run
	list1_shuf = []
	list2_shuf = []
	index_shuf = range(len(list1))
	shuffle(index_shuf)
	for i in index_shuf:
	    list1_shuf.append(list1[i])
	    list2_shuf.append(list2[i])
	return list1_shuf, list2_shuf

def divide_list_by_ratio(A, ratio=3): # so the smaller list is 1/3 the size of the original
	''' Takes list param and returns (bigger, smaller) according to TRAIN_TEST_RATIO. '''
	l = len(A)
	B = A[:l-l/ratio]
	C = A[l-l/ratio:]
	return B, C
def db_symbol_change(symbol, date):
	daynum = date.weekday()
	if daynum == 0: # if monday
		prevdate = date - timedelta(days=3)

	elif daynum == 5: # if saturday
		prevdate = date - timedelta(days=1)
		date += timedelta(days=2)

	elif daynum == 6: # if sunday
		prevdate = date - timedelta(days=2)
		date += timedelta(days=1)

	else: # if Tuesday - Friday
		prevdate = date - timedelta(days=1)

	# print "-"*30
	# print date, "====>", date.weekday()
	# print prevdate, "====>", prevdate.weekday()

	date_str = date.strftime('%Y-%m-%d')
	prevdate_str = prevdate.strftime('%Y-%m-%d')

	db = sqlite3.connect('Resources/articles.db')
	c = db.cursor()
	r1 = list(c.execute("select price from quotes where symbol = '"+symbol+"' and date = '"+prevdate_str+"'"))
	r2 = list(c.execute("select price from quotes where symbol = '"+symbol+"' and date = '"+date_str+"'"))

	db.close()

	if len(r1) == 0 or len(r2) == 0:
		return False
	else:
		p1 = float(r1[0][0])
		p2 = float(r2[0][0])
		return (p2 - p1) / (.5 * (p1 + p2)) * 100

	# print prevdate_str, p1, date_str, p2
def yahoo_symbol_change(symbol, date):
	"""Pulls data from Yahoo's API and calculates the percent change from the start data to the end date."""

	daynum = date.weekday()
	if daynum == 0: # if monday
		prevdate = date - timedelta(days=3)

	elif daynum == 5: # if saturday
		prevdate = date - timedelta(days=1)
		date += timedelta(days=2)

	elif daynum == 6: # if sunday
		prevdate = date - timedelta(days=2)
		date += timedelta(days=1)

	else: # if Tuesday - Friday
		prevdate = date - timedelta(days=1)

	date_str = date.strftime('%Y-%m-%d')
	prevdate_str = prevdate.strftime('%Y-%m-%d')

	q = 'select * from yahoo.finance.historicaldata where symbol = "%s" and startDate = "%s" and endDate = "%s"' % (symbol, date_str, prevdate_str)
	query = urllib.quote_plus(q)

	# Format URL for YQL
	url = "http://query.yahooapis.com/v1/public/yql?q=" + query + "&env=http%3A%2F%2Fdatatables.org%2Falltables.env"

	# Launch Yahoo Request
	r = BeautifulSoup(requests.get(url).text)
	symbols = r.find_all("symbol")

	# If YQL Api is not down, simply calculate percent change
	if(len(symbols) > 0): 
		p2 = float(symbols[0].close.string)
		p1 = float(symbols[1].close.string)
		return (p2 - p1) / (.5 * (p1 + p2)) * 100
	else: # Otherwise call the ystocksymbol package
		self.data = ystockquote.get_historical_prices(symbol, convert_date(date_str), convert_date(prevdate_str))
		days = len(self.data) - 1
		p2 = float(self.data[1][4])
		p1 = float(self.data[days][4])
		return (p2 - p1) / (.5 * (p1 + p2)) * 100

def convert_date(date):
	return date.replace("-", "")
