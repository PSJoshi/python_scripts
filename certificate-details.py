#!/usr/bin/env python
import subprocess
import logging
import os
import sys
from urlparse import urlparse

"""
# use of openssl for ssl certificate details
psj@psj-desktop:~/Downloads/nmap-6.40$ openssl s_client -showcerts -connect google.com:443</dev/null

Certificate validity:
psj@psj-desktop:~/Downloads/nmap-6.40$ openssl s_client -showcerts -connect google.com:443</dev/null |openssl x509 -noout -dates

Issuer details:
psj@psj-desktop:~/Downloads/nmap-6.40$ openssl s_client -showcerts -connect google.com:443</dev/null |openssl x509 -noout -issuer

Subject:
psj@psj-desktop:~/Downloads/nmap-6.40$ openssl s_client -showcerts -connect google.com:443</dev/null |openssl x509 -noout -subject

SHA-1 Fingerprint:
psj@psj-desktop:~/Downloads/nmap-6.40$ openssl s_client -showcerts -connect google.com:443</dev/null |openssl x509 -noout -fingerprint

# use NMAP for ssl related details
psj@psj-desktop:~/Downloads/nmap-6.40$ export SET NMAPDIR=/home/psj/Downloads/nmap-6.40/

Get SSL certificate details
psj@psj-desktop:~/Downloads/nmap-6.40$ nmap google.com -PN -T4 -p 443 --script=ssl-cert

Get cipher details
psj@psj-desktop:~/Downloads/nmap-6.40$ nmap google.com -PN -T4 -p 443 --script=ssl-enum-ciphers

"""


# logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

def command_response(domain,cert_command):
	cmd = '/usr/bin/openssl s_client -showcerts -connect %s:443</dev/null |openssl x509 -noout -%s' %(domain,cert_command)
	response = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
	process_response = response.communicate()[0]
	return process_response

def get_dates(domain):
	start = end = None	
	domain_response = command_response(domain,'dates')
	if domain_response:
		split_response = domain_response.split('\n')[:-1]
		logger.info("Issue date: %s Expiry date: %s "%(split_response[0],split_response[1]))
		start,end = split_response[0].split('=')[1],split_response[1].split('=')[1]
	return start,end

def get_issuer(domain):
	issuer = None
	domain_response = command_response(domain,'issuer')
	if domain_response:
		split_response = domain_response.split('\n')[:-1]
		issuer = split_response[0]
	return issuer

def get_subject(domain):
	subject = None
	domain_response = command_response(domain,'subject')
	if domain_response:
		split_response = domain_response.split('\n')[:-1]
		subject = split_response[0]
	return subject

def get_fingerprint(domain):
	fingerprint = None
	domain_response = command_response(domain,'fingerprint')
	if domain_response:
		split_response = domain_response.split('\n')[:-1]
		fingerprint = split_response[0]
	return fingerprint

if __name__ == '__main__':

	# extract domain from url
	url_details = urlparse('http://www.google.com')
	domain = url_details.netloc
	
	# check if openssl is installed or not
	if os.path.isfile('/usr/bin/openssl'):
		issue_date,expiry_date = get_dates(domain)
		logger.info("Certificate issue date:%s" % issue_date)
		logger.info("Certificate expiry date:%s" % expiry_date)
	else:
		logger.info("Openssl package is not present on the system. The program can not continue... Quitting...")

	issuer = get_issuer(domain)
	logger.info("Certificate issuer - %s" %issuer)
	sub = get_subject(domain)
	logger.info("Certificate subject - %s" %sub)
	fingerprint = get_fingerprint(domain)
	logger.info("Certificate fingerprint - %s" %fingerprint)

