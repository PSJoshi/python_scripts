#!/usr/bin/env python
import psutil
import netifaces
import sys
import logging
import subprocess

# Add various metrics from this code - https://gitlab.ncl.ac.uk/cs-support-group/lcd-monitor-panel/blob/master/data.py

# logging
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_kernel_modules_details():
	response = subprocess.Popen('lsmod',stdout=subprocess.PIPE,shell=False)
	process_response = response.communicate()[0]
	kernel_modules = process_response.split('\n')[:-1]
	#remove header
	kernel_modules=kernel_modules[1:]
	total_kernel_modules = len(kernel_modules)
	kernel_module_details = list()
	kernel_module_headers = ['name','size','count']
	for module in kernel_modules:
		module_details = module.split(' ') # space seperator
		module_details = [s for s in module_details if s != '']
		kernel_module_details.append(zip(kernel_module_headers,module_details))
		logger.info("Kernel module details - %s" %zip(kernel_module_headers,module_details))
	return total_kernel_modules,kernel_module_details

def Isrunning(process_name):
	for proc in psutil.process_iter():
		try:
			if proc.name() == process_name and proc.status() == 'running':
				return True
			logger.debug("process %s is %s" %(proc.name(),proc.status()))
		except (psutil.AccessDenied, psutil.NoSuchProcess):
			pass
	return False

def get_nw_interfaces():
	return netifaces.interfaces()

def nw_interface_details(nw_interface_name):
	interface_ipv4_details = None
	interface_mac_details = None 
	interface_ipv6_details = None
	try:
		interface_addr_details = netifaces.ifaddresses(nw_interface_name)
		# Interface - IPv4 address details, MAC details, IPv6 details
		interface_ipv4_details = interface_addr_details[netifaces.AF_INET]
		logger.info("IPv4 details - %s" %interface_ipv4_details)
		interface_mac_details = interface_addr_details[netifaces.AF_LINK]
		logger.info("MAC details - %s" %interface_mac_details)
		interface_ipv6_details = interface_addr_details[netifaces.AF_INET6]
		logger.info("IPv6 details - %s" %interface_ipv6_details)
	except Exception:
		pass
	return interface_ipv4_details,interface_mac_details,interface_ipv6_details

def get_interface_status(nw_interface_name):
	try:
		# you can also use command - ip a show ethX up
		cmd = 'cat /sys/class/net/%s/operstate' % nw_interface_name
		response = subprocess.Popen(cmd.split(' '),stdout = subprocess.PIPE, shell=False)
		process_response = response.communicate()[0]
		logger.info("Response for command - cat /sys/class/net/%s/operstate is %s" % (nw_interface_name,process_response))
		if process_response.strip().lower() == 'up':
			return True
		else: return False
	except Exception, e:
		logger.info("Error while getting %s interface status - %s" %(nw_interface_name,str(e)),exc_info=True)

def get_promiscous_status(nw_interface_name):
	try:
		# if Flags column contains 'I', it is promiscous.
		# https://it.awroblew.biz/linux-how-to-checkenable-promiscuous-mode/
		cmd = 'netstat -i'
		response = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE,shell=False)
		process_response = response.communicate()[0]
		# skip headers
		nw_interface_list = process_response.split('\n')[2:-1]
		for i_face in nw_interface_list:
			iface_columns = i_face.split()	
			if nw_interface_name in iface_columns[0].strip():
				logger.info("%s Interface flags - %s" %(nw_interface_name,iface_columns[11]))
				if "I" in iface_columns[11].strip():
					return True # interface is promiscous
		return False
				
	except Exception,e:
		logger.info("Error while getting promiscous state status for interface - %s : %s"%(nw_interface_name,str(e)),exc_info=True)

if __name__ == "__main__":

	# check if process is running or not
	print Isrunning('firefox')

	# Kernel modules
	total_kernel_mods,kernel_mods = get_kernel_modules_details()
	#print total_kernel_mods,kernel_mods
	for item in kernel_mods:
		# print kernel module - name,size, and count
		print dict(item)

	# interface details
	network_interfaces = get_nw_interfaces()
	for iface in network_interfaces:
		iface_results = nw_interface_details(iface)
		print "Interface results: \n %s " %str(iface_results)
		iface_status = get_interface_status(iface)
		print "Interface status - %s" % iface_status

	# check if interface is in promiscous mode or not.
	network_interfaces = get_nw_interfaces()
	for iface in network_interfaces:
		promiscous_status = get_promiscous_status(iface)
		print "Interface-%s   promiscous status-%s " %(iface, promiscous_status)


	sys.exit(1)
	

