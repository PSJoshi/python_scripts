#!/usr/bin/env python
import requests
import sys
import logging
import StringIO

# tor exit nodes urls
tor_urls = 'https://check.torproject.org/exit-addresses'
tor_dan_uk_urls = 'https://www.dan.me.uk/torlist/'

# logging
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logger = logging.getLogger(__name__)

def download_tor_nodes(url):
	"""
	Download tor exit nodes from official tor site - https://check.torproject.org/exit-addresses 	
	"""
	try:	
		response = requests.get(url)
		logging.info("Tor Exit nodes from https://check.torproject.org/exit-addresses :%s"%response.text)
		tor_node_list = list()
		if response.text:	
			buf = StringIO.StringIO(response.text)		
			for line in buf.readlines():
				if line.startswith("ExitAddress"):# parse lines with IP address
					tor_ip = line.strip().split()[1]
					tor_node_list.append(tor_ip)					
					logging.info(tor_ip)
		return tor_node_list

	except Exception:
		logging.error("Error while downloading tor exit nodes",exc_info=True)


def download_tor_dan_uk_list(url):
	"""
	Download tor exit nodes from official tor site - https://check.torproject.org/exit-addresses 	
	"""
	try:	
		response = requests.get(url)
		logging.info("Tor Exit nodes from UK site - https://www.dan.me.uk/torlist/ :%s"%response.text)
		tor_node_list = list()
		if response.text:	
			buf = StringIO.StringIO(response.text)		
			for line in buf.readlines():
				tor_node_list.append(line.strip())
				logging.info(line.strip())
		return tor_node_list

	except Exception:
		logging.error("Error while downloading tor exit nodes",exc_info=True)
				
if __name__ == "__main__":

	#tor_node_list = download_tor_nodes(tor_urls)
	tor_node_list = download_tor_dan_uk_list(tor_dan_uk_urls)
	print tor_node_list

