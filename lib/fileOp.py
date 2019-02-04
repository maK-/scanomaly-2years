#This class does required file in/out operations
#
# Read file to list
# example = FileOp(file).reader()
#
#Write list to file
# FileOp(file).writer(example)

import sys

class FileOp:
    def __init__(self, name):
        self.fname = name
    
    def reader(self):
        try:
            with open(self.fname) as f:
                data = f.read().splitlines()
        except IOError:
            print('File IO Error!')
            sys.exit(0)
        return data

    def writer(self, wobj):
        try:
            f = open(self.fname, 'w')
            #If a list
            if hasattr(wobj, '__iter__'):
                for i in wobj:
                    f.write(i+'\n')
            #Else a string
            else:
                f.write(wobj+'\n')
            f.close
        except IOError:
            print('File IO Error!')
