#!/usr/bin/env python
"""
This script downloads Alexia Top 1 million sites and generates a CSV file.
It also allows you to return Top N sites.
"""
import zipfile
import StringIO
import requests

ALEXIA_URL = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

def get_alexia_urls():
	"""
	   Download and generate Alexia top 1 million url lists
	"""
	#download top 1 million site urls
	zip_top_urls = requests.get(ALEXIA_URL)
	response_buf = StringIO.StringIO(zip_top_urls.content)
	# unzip contents
	zfile = zipfile.ZipFile(response_buf)
	buf = StringIO.StringIO(zfile.read('top-1m.csv'))

	for line in buf.readlines():
		(rank,domain) = line.split(',')
		yield (int(rank),domain.strip())

def top_url_list(num_sites=100):
	urls = get_alexia_urls()
	return [urls.next() for x in xrange(num_sites)]

if __name__ == "__main__":
	print top_url_list()
