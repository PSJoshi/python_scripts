#!/usr/bin/env python

# This script is used to determine certificate expiry date.
# It can be used to raise alerts to host/system admins.

# Install using pip3 install pyOpenSSL
import OpenSSL
import ssl
import argparse
import logging
import sys
import argparse

# setup logging
logging.basicConfig(stream=sys.stdout,level = logging.DEBUG)
logger = logging.getLogger(__name__)

def cmd_arguments():
    try:
        parser = argparse.ArgumentParser("This script is used to check certificate expiry of the domain")
        parser.add_argument('--domain', required=True, help='Please specify domain name!',dest='domain')
    except Exception as exc:
        logger.error("Error while getting command line arguments - %s" %exc.message, exc_info=True)

def get_certificate_expiry(domain):
    expiry_date = None
    try:
        cert = ssl.get_server_certificate((domain,443))
        x509_format = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        x509_expiry_info = x509_format.get_notAfter()
        # print(x509_format.get_subject())
        # print(x509_format.has_expired())
        expiry_day = x509_expiry_info[6:8].decode(‘utf-8’)
        expiry_month = x509_expiry_info[4:6].decode(‘utf-8’)
        expiry_year = x509_expiry_info[:4].decode(‘utf-8’)

        expiry_date = str(exp_day) + “-” + str(exp_month) + “-” + str(exp_year)
        
    except Exception as exc:
        logger.error("Error while getting certificate information - %s" %exc.message, exc_info=True)         
    
    return expiry_date
        
if __name__ == "__main__":
    try:
        cmd_args = cmd_arguments()
        if cmd_args.domain == None:
            logger.info("Please enter domain name for checking certificate expiry date")
            sys.exit(1)
        print("Certificate expiry for domain - %s is %s", (%cmd_args.domain, get_certificate_expiry(cmd_args.domain)))
             
    except Exception as exc:
        logger.error("Error while checking certificate expiry information - %s" %exc.message,exc_info=True)
     
