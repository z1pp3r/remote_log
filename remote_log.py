import os
import sys
from itertools import repeat

class Parser():
    def __init__(self,filename=None,blocksize = 1):
        self.__filename = filename
        self.__file_inode = 0
        self.__fd = None
        self.__block_size = blocksize

    def __del__(self):
        self.__closeFile()

    def __handleData(self):
        pass

    def __reload_file(self):
        self.__closeFile()
        self.__loadFile()

    def __loadFile(self):
        try:
            self.__fd = os.open(self.__filename,os.O_RDONLY|os.O_APPEND)
        except Exception,msg:
            sys.stderr.write('Error opening file: '+str(msg)+'\n')
            self.__fd = None

    def __closeFile(self):
        try:
            os.close(self.__fd)
        except Exception,msg:
            sys.stderr.write('Error closing file: '+str(msg)+'\n')

    def getFileName(self):
        return self.__filename

    def setFileName(self,filename):
        self.__filename = filename

    def setDataHandler(self,handler):
        self.__handleData = handler

    def getDataHandler(self):
        return self.__handleData

    def test(self,string):
        self.__handleData(string)

    def setBlockSize(self,size):
        self.__block_size = size

    def getBlockSize(self):
        return self.__block_size

    def __isFileExists(self):
        try:
            __cur_fd =  os.fstat(self.__filename).st_ino
        except:
            return False
        else:
            if __cur_fd!= self.__file_inode:
                return False
            else:
                return True

    def __check(self):
        if self.__filename is None:
            raise AttributeError('Error: filename cannot be empty')
            return False
        if self.__block_size<=0:
            raise AttributeError('Error: block size must be greater than 1')
            return False
        return True

    def start(self):
        if not self.__check():
            pass
        else:
            self.__loadFile()
            print 1
            old_data = ''
            if not self.__isFileExists():
                self.__reload_file()