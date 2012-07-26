import os
import sys
import time
import socket

class Parser(object):
    def __init__(self,filename=None,**kwargs):
        self.__filename = filename
        self.__file_inode = 0
        self.__fd = None
        self.__block_size = kwargs.get('blocksize',1)
        self.__delimiter = kwargs.get('delimiter','56')

    def __del__(self):
        self.__closeFile(silent=True)

    def __handleData(self,string):
        print string

    def __reload_file(self):
        if self.__fd is not None:
            self.__closeFile()
        self.__loadFile()

    def __loadFile(self,silent=False):
        try:
            self.__fd = os.open(self.__filename,os.O_RDONLY|os.O_APPEND)
            self.__file_inode = os.fstat(self.__fd).st_ino
        except Exception,msg:
            if not silent: sys.stderr.write('Error opening file: '+str(msg)+'\n')
            self.__fd = None
            time.sleep(1)

    def __closeFile(self,silent=False):
        try:
            os.close(self.__fd)
        except Exception,msg:
            if not silent: sys.stderr.write('Error closing file: '+str(msg)+'\n')

    def getFileName(self):
        return self.__filename

    def setFileName(self,filename):
        self.__filename = filename

    def setDataHandler(self,handler):
        self.__handleData = handler

    def getDataHandler(self):
        return self.__handleData

    def test(self):
        __msg = []
        __result = True
        if (self.__filename is None):
            __msg.append('Filename is empty')
            __result = False
        if (self.__block_size<=0):
            __msg.append('Block size must br greater than zero')
            __result = False
        return (__result,';'.join(__msg))

    def setBlockSize(self,size):
        self.__block_size = size

    def getBlockSize(self):
        return self.__block_size

    def __isFileExists(self):
        try:
            __cur_fd =  os.stat(self.__filename).st_ino
        except:
            return False
        else:
            if __cur_fd!= self.__file_inode:
                return False
            else:
                return True

    def setDelimiter(self,delimiter):
        self.__delimiter = delimiter

    def getDelimiter(self):
        return self.__delimiter

    def __start(self):
        __status_ok,_ = self.test()
        if not __status_ok:
            pass
        else:
            old_data = ''
            while True:
                if not self.__isFileExists():
                    self.__reload_file()
                data = old_data + os.read(self.__fd,self.__block_size)
                if len(data)==0:
                    time.sleep(0.1)
                    continue
                try:
                    last_index = len(data)-data[::-1].index(self.__delimiter[::-1])-len(self.__delimiter)
                except ValueError:
                    old_data = data
                    continue
                else:
                    old_data = data[last_index+len(self.__delimiter):]
                    data = data[:last_index].split(self.__delimiter)
                    for line in data:
                        self.__handleData(' '.join(line.split()))

    def start(self):
        try:
            self.__start()
        except KeyboardInterrupt:
            print 'Exiting'

class carbon_client(object):
    def __init__(self,**kwargs):
        self.__carbon_host = kwargs.get('host','127.0.0.1')
        self.__carbon_port = kwargs.get('port',2003)
        self.__connect()
        self.__hostname = socket.gethostname().replace('.','_')

    def __del__(self):
        pass

    def __connect(self):
        self.__socket = socket.socket()
        self.__socket.connect(self.__carbon_host,self.__carbon_port)

    def __disconnect(self):
        self.__socket.close()

    def __reconnect(self):
        self.__disconnect()
        self.__connect()

    def send(self,name,value,time):
        __message = '%s.%s %s %s\n' % (name,self.__hostname,value,time)
        self.__socket.send(__message)