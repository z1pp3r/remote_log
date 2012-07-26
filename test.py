#!/usr/bin/env python

import re

from remote_log import Parser

def handler(string):
    if re.match(r'^1.*$',string):
        print 'asd',string
    else:
        print 'def',string


parser = Parser('/home/litvinov/testfile2')
parser.setDataHandler(handler)

is_ok,msg = parser.test()

print parser.getFileName()

parser.start()
