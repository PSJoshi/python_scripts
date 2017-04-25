#!/usr/bin/env python
import requests
import hashlib
import argparse
import logging
import sys

# To run - $python hash-webpage.py --url http://mygov.in

# adjust your logging options as per recommendations here:
# http://stackoverflow.com/questions/15727420/using-python-logging-in-multiple-modules
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def cmd_options():
    args = None
    try:
        parser = argparse.ArgumentParser(
            description="""This script computes the hash of webpage and can be
			used to check if the page has changed since the last run.
                        """)
        parser.add_argument('--url', action='store', required=True,
            help='Enter the url', dest='url')
        args,unknown = parser.parse_known_args()

    except Exception,e:
        logger.error("Error while parsing command line arguments - %s"
            % e.message, exc_info=True)

    return args

def main(check_url):
	page_contents = requests.get(check_url)
	response = page_contents.text
	return hashlib.sha256(response.encode('utf-8')).hexdigest()

if __name__ == '__main__':
	try:
		cmd_args = cmd_options()
		hash_val = main(cmd_args.url)
		logger.info("Hash for url - %s is %s" %(cmd_args.url, hash_val))
	except Exception as e:
		logger.error("Error while running the script - %s" % e.message, exc_info=True)
