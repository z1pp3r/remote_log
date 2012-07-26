#!/usr/bin/env python

import os
import sys
import time
from socket import socket
import re

def sendData(now,line):
    message = 'test.random_value %s %s\n' % (line,now)
 #   sock.sendall(message)
    print message


SERVER = "10.7.33.23"
PORT = 2003
DELIMITER = '</log-entry>'
FILE_NAME = '/var/log/processing/requests/online_all_queries.log'
STRING_REGEXP = r'^<log-entry date="([0-9a-zA-Z\ :"]+)">.*<dispatch-time-in-ms>([0-9]+)</dispatch-time-in-ms>$'
BLOCKSIZE = 1024*1024

sock = socket()
try:
    sock.connect( (SERVER,PORT) )
except:
    print "Couldn't connect to %(server)s on port %(port)d" % { 'server':SERVER, 'port':PORT }
    sys.exit(1)

fd = os.open(FILE_NAME,os.O_RDONLY|os.O_APPEND)
old_data = ''

while True:
    try:
        FILE_INODE = os.stat(FILE_NAME).st_ino
    except Exception,msg:
#        print 'Error:',msg
        pass
    else:
        if os.fstat(fd).st_ino!= FILE_INODE:
            os.close(fd)
            fd = os.open(FILE_NAME,os.O_RDONLY|os.O_APPEND)
        data = old_data + os.read(fd,BLOCKSIZE)
        if len(data)==0:
            continue
        try:
            last_index = len(data)-data[::-1].index(DELIMITER[::-1])-len(DELIMITER)
        except ValueError:
            old_data = data
            continue
        old_data = data[last_index+len(DELIMITER):]
        data = ' '.join(data[:last_index].split()).split(DELIMITER)
        for i in data:
            string = i.strip()
            print len(string),re.findall(STRING_REGEXP,string)
#        print data,os.fstat(fd).st_ino
#        for i in data:
#            sendData(time.time(),i)