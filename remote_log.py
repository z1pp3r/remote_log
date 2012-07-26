import os
import sys
import time
import threading

class Parser(threading.Thread):
    def __init__(self,filename=None,blocksize = 1024):
        self.__filename = filename
        self.__file_inode = 0
        self.__fd = None
        self.__block_size = blocksize

    def __del__(self):
        self.__closeFile(silent=True)

    def __handleData(self):
        pass

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


    def start(self):
        __status_ok,_ = self.test()
        if not __status_ok:
            pass
        else:
            old_data = ''
            while True:
                if not self.__isFileExists():
                    self.__reload_file()
                data = os.read(self.__fd,self.__block_size)
                if len(data)>0:
                    print data
                elif len(data)<self.__block_size:
                    time.sleep(0.5)
