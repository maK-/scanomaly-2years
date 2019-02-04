#This module is used to directory bust with a common directory list
from yapsy.IPlugin import IPlugin
from lib.requestObject import RequestObject
from lib.fileOp import FileOp
from lib.dataparser import ParseArguments
from lib.urlObject import UrlObject
import random

class Dirb(IPlugin):
    def gen(self, cwd, urls, proxy, headers, timeout, cookies, 
            postdata, module):
        requestList = []    #Store generated request objects
        data = FileOp(cwd+'/lists/dirs.txt').reader()
        shuffled = random.shuffle(data) #Randomize our list
        newurl = ''
        for url in urls:
            u = UrlObject(url)
            for directory in data:
                newurl = u.u_d+directory
                req_get = RequestObject('reqID','GET', proxy, headers, timeout,
                                        cookies, newurl, postdata, module)
                requestList.append(req_get)
        return requestList
