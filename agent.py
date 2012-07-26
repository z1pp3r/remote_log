#!/usr/bin/env python

import os
import sys
import time
import socket
import re

def sendData(now,line,name):
    message = 'connection_holding_time_%s.%s %s %s\n' % (name,HOSTNAME,line,now)
    sock.sendall(message)
    print message

HOSTNAME = socket.gethostname().replace('.','_')
SERVER = "10.7.33.23"
PORT = 2003
DELIMITER = '====================================='
FILE_NAME = '/var/log/processing/db/online_connections_holding_times.log'
#STRING_REGEXP = r'^<log-entry date="([0-9a-zA-Z\ :"]+)">.*<dispatch-time-in-ms>([0-9]+)</dispatch-time-in-ms>$'
STRING_REGEXP = r'^Date: ([0-9a-zA-Z\ :"]+) Connection holding time:\ ([0-9]+) Pool: \w+@(\w+).*$'
BLOCKSIZE = 1024*1024

sock = socket.socket()
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
            i = i.strip()
            if len(i)==0:
                continue
            i = re.findall(STRING_REGEXP,i)[0]
            now = time.mktime(time.strptime(i[0],'%d %b %Y %H:%M:%S'))
            value = i[1]
            name = i[2]
            sendData(now,value,name)