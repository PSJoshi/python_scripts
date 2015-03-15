#!/usr/bin/env python
"""
	This module use dnspython, a powerful DNS toolkit for python - http://www.dnspython.org
	The module provides functions for various DNS records like A,NS,MX,TXT,PTR and SOA. 
"""
import dns.resolver
from dns import reversename
import time
import sys

def dns_A_records(domain):
	a_records = list()
	ttl = None
	num_records = None
	try:
		dns_results = dns.resolver.query(domain, 'A')
		ttl = dns_results.ttl
		num_records = len(dns_results)
		if dns_results.rrset:
			for x in dns_results.rrset:
				a_records.append(x.to_text())
	except Exception:
		pass
	return num_records,a_records,ttl

def dns_NS_records(domain):
	ns_records = list()
	ttl = None
	num_records = None
	try:
		dns_results = dns.resolver.query(domain, 'NS')
		ttl = dns_results.ttl
		num_records = len(dns_results)
		if dns_results.rrset:
			for x in dns_results.rrset:
				ns_records.append(x.to_text())
	except Exception:
		pass
	return num_records,ns_records,ttl


def dns_MX_records(domain):
	mx_records = list()
	ttl = None
	num_records = None
	try:
		dns_results = dns.resolver.query(domain, 'MX')
		ttl = dns_results.ttl
		num_records = len(dns_results)
		if dns_results.rrset:
			for x in dns_results.rrset:
				mx_records.append(x.to_text().split(' ')[1])
	except Exception:
		pass	
	return num_records,mx_records,ttl

def dns_CNAME_records(domain):
	cname_records = list()
	ttl = None
	num_records = None
	try:
		dns_results = dns.resolver.query(domain, 'CNAME')
		ttl = dns_results.ttl
		num_records = len(dns_results)
		if dns_results.rrset:
			for x in dns_results.rrset:
				cname_records.append(x.target.to_text())
	except Exception:
		pass
	return num_records,cname_records,ttl
		
def dns_TXT_records(domain):
	txt_records = list()
	ttl = None
	num_records = None
	try:
		dns_results = dns.resolver.query(domain, 'TXT')
		ttl = dns_results.ttl
		num_records = len(dns_results)
		if dns_results.rrset:
			for x in dns_results.rrset:
				txt_records.append(x.to_text())
	except Exception:
		pass
	return num_records,txt_records,ttl

def dns_SOA_records(domain):
	soa_records = list()
	ttl = None
	num_records = None
	try:
		dns_results = dns.resolver.query(domain, 'SOA')
		ttl = dns_results.ttl
		num_records = len(dns_results)
		if dns_results.rrset:
			for x in dns_results.rrset:
				soa_records.append([x.serial,x.refresh,x.expire,x.retry])
	except Exception:
		pass
	return num_records,soa_records,ttl

def dns_PTR_records(ip):
	ptr_records = list()
	ttl = None
	num_records = None
	try:
		addr = reversename.from_address(ip)
		ptr_results = dns.resolver.query(addr,"PTR")
		num_records = len(ptr_results)
		if ptr_results.rrset:
			for x in ptr_results.rrset:
				ptr_records.append(x.to_text())
	except Exception:
		pass
	return num_records,ptr_records,ttl

if __name__=="__main__":
	num_records,records,ttl = dns_PTR_records('173.194.36.37')
	print num_records,records,ttl
	num_records,records,ttl = dns_NS_records('google.com')
	print num_records,records,ttl
	time.sleep(1)	
	num_records,records,ttl = dns_MX_records('google.com')
	print num_records,records,ttl
	time.sleep(1)	
	num_records,records,ttl = dns_A_records('google.com')
	print num_records,records,ttl
	time.sleep(1)	
	num_records,records,ttl = dns_CNAME_records('mail.google.com')
	print num_records,records,ttl
	time.sleep(1)
	num_records,records,ttl = dns_TXT_records('google.com')
	print num_records,records,ttl
	time.sleep(1)
	num_records,records,ttl = dns_SOA_records('google.com')
	print num_records,records,ttl

