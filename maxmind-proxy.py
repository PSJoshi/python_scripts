#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
'''
This script fetches high risk IP addresses list from MaxMind. This list
is updated twice monthly.
'''
r = requests.get('https://www.maxmind.com/en/high-risk-ip-sample-list')
soup = BeautifulSoup(r.text)
for link in soup.findAll('a', {'class': 'span3'}):
	try:	
		print link.string
	except KeyError:
		pass


