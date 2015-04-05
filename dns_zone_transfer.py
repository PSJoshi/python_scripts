#!/usr/bin/python
import dns.resolver
import dns.query
import dns.zone
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--domain',action = 'store',help = 'Enter domain')

args = parser.parse_args()

if args.domain:
	domain = args.domain
else:
	domain = None

if not domain:
	print "The domain that you have entered is not valid. Quitting..."
	sys.exit(1)

query_ns = dns.resolver.query(domain,'NS')
try:
	for ns in query_ns.rrset:
		#strip . at the end
		nameserver_name = str(ns)[:-1]
		if nameserver_name is None or nameserver_name == "" :
			continue
		try:
			xfr_query = dns.query.xfr(nameserver_name,domain)
			try:
				zone = dns.zone.from_xfr(xfr_query)
				if zone is None:
					continue
				for name, node in zone.nodes.items():
					for r_dataset in node.rdatasets:
						print "zone - %s" %str(r_dataset)
			except Exception,e:
				#print e
				continue
		except Exception,e:
			#print e
			continue
except Exception,e:
	#print e
	pass
