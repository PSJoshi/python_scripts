import subprocess

""" If the program is running "ps -ef | grep program" will return 2 or more rows 
(one with the program itself and the second one with "grep program"). 
Otherwise, it will only return one row ("grep program") 
You can trigger the alert on this if required.
"""

def monitor_process(name):
	args=['ps','-ef']
	args1=['grep','-c','%s' %name]
	process_ps = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
	process_monitor = subprocess.Popen(args1, stdin=process_ps.stdout, stdout=subprocess.PIPE, shell=False)
	# Allow process_ps to receive a SIGPIPE if process_monitor exits.
	process_ps.stdout.close()
	return process_monitor.communicate()[0]


if __name__== "__main__":
	print monitor_process('firefox')
