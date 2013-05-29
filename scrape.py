import sqlite3
import re
import requests
import csv
import StringIO

conn = sqlite3.connect("stocks.db")

cursor = conn.cursor()

# cursor.execute("""CREATE TABLE prices (symbol text, date text, open text, high text, low text, close text, volume text, adj_close text) """)

number = cursor.execute('SELECT count(*) FROM stocks')
num = 0
for n in number:
    num = n[0]
count = 0
data = cursor.execute('SELECT * FROM stocks')
for d in data:
    print "%2.1f/100: Fetching quote for %s" % (float(count) / num * 100, d[0])

    symbol = d[0]
    url = "http://finance.yahoo.com/q/hp?s=" + symbol

    r = requests.get(url).text
    search = "<a href=\"(http:\/\/ichart\.finance.\yahoo\.com\/table.csv\?s\=[A-Z]+&amp;d=[0-9]+&amp;e=[0-9]+&amp;f=[0-9]+&amp;g=d&amp;a=[0-9]+&amp;b=[0-9]+&amp;c=[0-9]+&amp;ignore=\.csv)\">"
    csv_url = re.search(search, r)
    if csv_url:
        csv_url = csv_url.group(1)
        csv_url = csv_url.replace("&amp;", "&")
        # print csv_url
        r = requests.get(csv_url).text
        # print r
        f = StringIO.StringIO(r)
        read = csv.reader(f, delimiter=',')
        curInner = conn.cursor()
        for row in read:
            s = 'INSERT INTO prices VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (symbol, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            curInner.execute(s)
    else:
        print "No data found!"
    count += 1
conn.close()
