#!/usr/bin/env python

import os
import sys
import time
from socket import socket

def sendData(now,line):
    message = 'test.random_value %s %s\n' % (now,line)
    sock.sendall(message)
    '''
    now = int( time.time() )
    lines = []
    #We're gonna report all three loadavg values
    loadavg = get_loadavg()
    lines.append("system.loadavg_1min %s %d" % (loadavg[0],now))
    lines.append("system.loadavg_5min %s %d" % (loadavg[1],now))
    lines.append("system.loadavg_15min %s %d" % (loadavg[2],now))
    message = '\n'.join(lines) + '\n' #all lines must end in a newline
    print "sending message\n"
    print '-' * 80
    print message
    print
    sock.sendall(message)
    time.sleep(delay)
    '''


SERVER = "127.0.0.1"
PORT = 1234

sock = socket()
try:
    sock.connect( (SERVER,PORT) )
except:
    print "Couldn't connect to %(server)s on port %(port)d" % { 'server':SERVER, 'port':PORT }
    sys.exit(1)


FILE_NAME = '/home/litvinov/testfile'
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
        data = old_data + os.read(fd,256)
        if len(data)==0:
            continue
        last_index = len(data)-1-data[::-1].index('\n')
        old_data = data[last_index+1:]
        data = data[:last_index].split('\n')
        print data,os.fstat(fd).st_ino
        for i in data:
            sendData(time.time(),i)